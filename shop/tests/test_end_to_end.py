import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status

from shop.models import Order, Product
from users.models import CustomerProfile


@pytest.mark.django_db
def test_full_user_checkout_payment_flow(api_client, mailoutbox, product_factory):
    """
    End-to-end workflow:
      1. User registers -> activation + welcome email are sent.
      2. User activates account (we generate uid/token directly).
      3. User logs in -> obtains JWT access token.
      4. User adds an address -> CustomerProfile is created automatically.
      5. A Product exists in the database (created via product_factory).
      6. User adds that Product to their cart.
      7. User checks out -> order is set to AWAITING_PAYMENT and stock is reserved.
      8. Simulate payment webhook -> order is CONFIRMED, actual stock is decremented,
         reserved stock cleared, and invoice email sent.
      9. Confirm order status is CONFIRMED and invoice email is in mailoutbox.
    """

    # --------------------------------------------------
    # 1) Registration: POST /users/ (Djoser RegisterSerializer)
    # --------------------------------------------------
    registration_payload = {
        "email": "alice@example.com",
        "username": "alice",
        "password": "StrongP4ssw0rd!",
        "re_password": "StrongP4ssw0rd!",  # required by Djoser
        "first_name": "Alice",
        "last_name": "Wonderland",
    }
    resp_registration = api_client.post(
        reverse("user-list"), registration_payload, format="json"
    )
    assert resp_registration.status_code == status.HTTP_201_CREATED

    # expect at least 2 emails: activation + welcome
    assert len(mailoutbox) >= 2

    # --------------------------------------------------
    # 2) Activate account by generating uid/token (avoid fragile URL parsing)
    # --------------------------------------------------
    User = get_user_model()
    user = User.objects.get(email="alice@example.com")

    # generate valid uidb64 and token using Django's mechanisms
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    resp_activation = api_client.post(
        reverse("user-activation"), {"uid": uidb64, "token": token}, format="json"
    )
    assert resp_activation.status_code == status.HTTP_204_NO_CONTENT

    # --------------------------------------------------
    # 3) Login: POST /auth/jwt/create/ (TokenObtainPairSerializer)
    # --------------------------------------------------
    login_payload = {"email": "alice@example.com", "password": "StrongP4ssw0rd!"}
    resp_login = api_client.post(
        reverse("token_obtain_pair"), login_payload, format="json"
    )
    assert resp_login.status_code == status.HTTP_200_OK
    access_token = resp_login.data["access"]

    # attach JWT to client for authenticated requests
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")

    # --------------------------------------------------
    # 4) Add Address: POST /users/me/addresses/ (MeAddressListCreateView)
    # --------------------------------------------------
    address_payload = {
        "label": "Home",
        "street": "Main St",
        "number": "42",
        "zipcode": "1234AB",
        "city": "Amsterdam",
        "country": "Netherlands",
        "is_billing": True,
        "is_shipping": True,
    }
    resp_address = api_client.post(
        reverse("users:me-addresses"), address_payload, format="json"
    )
    assert resp_address.status_code == status.HTTP_201_CREATED

    # ensure CustomerProfile was created automatically
    profile = CustomerProfile.objects.filter(user__email="alice@example.com").first()
    assert profile is not None

    # --------------------------------------------------
    # 5) Ensure a Product exists in the DB via fixture
    # --------------------------------------------------
    product = product_factory(name="TestProduct", price=9.99, stock=5)
    assert isinstance(product, Product)

    # --------------------------------------------------
    # 6) Add Product to Cart: POST /cart/items/ (this should create a new order)
    # --------------------------------------------------
    add_to_cart_payload = {"product": str(product.pk), "quantity": 1}
    resp_add = api_client.post(
        reverse("shop:cart-items-list"), add_to_cart_payload, format="json"
    )
    assert resp_add.status_code == status.HTTP_201_CREATED

    # --------------------------------------------------
    # 7) Checkout: POST /cart/checkout/
    # --------------------------------------------------
    resp_checkout = api_client.post(reverse("shop:cart-checkout"), {}, format="json")
    # expect 204 No Content on successful checkout
    assert resp_checkout.status_code == status.HTTP_200_OK

    # retrieve the newly created order with status AWAITING_PAYMENT
    pending_orders = Order.objects.filter(
        user__email="alice@example.com", status=Order.StatusChoices.AWAITING_PAYMENT
    )
    assert pending_orders.exists()
    order = pending_orders.first()

    # verify reserved stock incremented, actual stock unchanged
    product.refresh_from_db()
    assert product.stock_reserved >= 1
    assert product.stock == 5

    # --------------------------------------------------
    # 8) Simulate Payment Webhook: POST /payment-webhook/
    # --------------------------------------------------
    mailoutbox.clear()  # clear previous emails; expect only the invoice email now.

    webhook_payload = {"order_id": str(order.order_id), "status": "paid"}
    resp_webhook = api_client.post(
        reverse("payment-webhook"),
        webhook_payload,
        format="json",
        HTTP_X_WEBHOOK_KEY=settings.WEBHOOK_SECRET_KEY,
    )
    assert resp_webhook.status_code == status.HTTP_200_OK

    # Verify order status is now CONFIRMED
    order.refresh_from_db()
    assert order.status == Order.StatusChoices.CONFIRMED

    # Verify actual stock decremented and reserved cleared
    product.refresh_from_db()
    assert product.stock == 4  # 5 - 1
    assert product.stock_reserved == 0

    # --------------------------------------------------
    # 9) Invoice Email Sent: exactly one email in mailoutbox
    # --------------------------------------------------
    assert len(mailoutbox) == 1
    invoice_email = mailoutbox[0]
    assert (
        "invoice" in invoice_email.subject.lower()
        or "order confirmed" in invoice_email.subject.lower()
    )
    assert "order #1" in invoice_email.body
    assert invoice_email.to == [order.user.email]
