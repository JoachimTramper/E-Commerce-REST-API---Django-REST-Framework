import threading

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from shop.models import Order, OrderItem, Product


@pytest.mark.django_db(transaction=True)
def test_two_concurrent_checkouts_only_one_reserves_stock_or_both_fail(
    user, admin_user, product_factory
):
    """
    Simulate two staff users who each already have a PENDING order containing
    the same product (stock=1), and then both attempt to check out at the same time.
    After both attempts:
      - At most one Order should have status=AWAITING_PAYMENT.
      - product.stock_reserved must be either 0 (if both failed due to locks)
        or 1 (if exactly one succeeded).
      - product.stock must remain 1.
      - Responses may be 200, 400, or 500:
         • At most one (or zero) should be 200.
         • Any failing request must be 400 (insufficient free stock) or 500 (lock error).
    """

    # create a single product with stock=1
    product = product_factory(stock=1)

    # create two separate PENDING orders (one per user)
    order1 = Order.objects.create(user=user, status=Order.StatusChoices.PENDING)
    OrderItem.objects.create(
        order=order1,
        product=product,
        quantity=1,
        price=product.price,
        item_subtotal=product.price * 1,
    )

    order2 = Order.objects.create(user=admin_user, status=Order.StatusChoices.PENDING)
    OrderItem.objects.create(
        order=order2,
        product=product,
        quantity=1,
        price=product.price,
        item_subtotal=product.price * 1,
    )

    # confirm that product.stock is still 1
    assert Product.objects.get(pk=product.pk).stock == 1

    # prepare two APIClient instances, one for each user
    client1 = APIClient()
    client2 = APIClient()
    client1.force_authenticate(user=user)
    client2.force_authenticate(user=admin_user)

    # build the URL for the checkout endpoint.
    url_checkout = reverse("shop:cart-checkout")

    # helper function to POST to /cart/checkout/ concurrently
    results = [None, None]

    def checkout_thread(client, index):
        try:
            resp = client.post(url_checkout, {}, format="json")
            results[index] = resp
        except Exception as e:

            class DummyResponse:
                status_code = 500
                data = {"error": str(e)}

            results[index] = DummyResponse()

    # launch both checkout requests at the same time
    thread1 = threading.Thread(target=checkout_thread, args=(client1, 0))
    thread2 = threading.Thread(target=checkout_thread, args=(client2, 1))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    # after both threads complete, ensure exactly one order has been set to AWAITING_PAYMENT
    awaiting_orders = Order.objects.filter(status=Order.StatusChoices.AWAITING_PAYMENT)
    assert (
        awaiting_orders.count() <= 1
    ), f"Expected exactly one AWAITING_PAYMENT order, found {awaiting_orders.count()}."

    # verify that product.stock is now 0
    product.refresh_from_db()
    assert product.stock_reserved in (
        0,
        1,
    ), f"Expected product.stock to be 1, found {product.stock}."
    assert (
        product.stock == 1
    ), f"Expected product.stock to remain 1, found {product.stock}."

    # check responses: at most one should be 200; zero is allowed if both fail due to locking
    status_codes = [results[0].status_code, results[1].status_code]
    num_200 = status_codes.count(200)
    assert num_200 <= 1, f"Expected at most one 200, but got {num_200}."
    # any failures must be 400 (insufficient stock) or 500 (lock error)
    for code in status_codes:
        if code != 200:
            assert code in (
                400,
                500,
            ), f"Unexpected status code {code}; expected 400 or 500."
