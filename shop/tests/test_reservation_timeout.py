from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

from shop.models import Order, OrderItem


@pytest.mark.django_db(transaction=True)
def test_reservation_expires_and_releases_stock(product_factory, user):
    # mark the first user as staff so they can perform checkout (if your permission setup requires it)
    user.is_staff = True
    user.save()

    # create a single Product with stock=1
    product = product_factory(stock=1)

    # create a PENDING Order for user1 with quantity=1
    order1 = Order.objects.create(user=user, status=Order.StatusChoices.PENDING)
    OrderItem.objects.create(
        order=order1,
        product=product,
        quantity=1,
        price=product.price,
        item_subtotal=product.price * 1,
    )

    client1 = APIClient()
    client1.force_authenticate(user=user)

    url_checkout = reverse("shop:cart-checkout")

    # checkout as user1 → should reserve stock_reserved=1
    resp1 = client1.post(url_checkout, {}, format="json")
    assert resp1.status_code == 200
    order1.refresh_from_db()
    assert order1.status == Order.StatusChoices.AWAITING_PAYMENT
    assert order1.reserved_until > timezone.now()
    product.refresh_from_db()
    assert product.stock_reserved == 1

    # create a second user and mark as staff
    from django.contrib.auth import get_user_model

    User = get_user_model()
    user2 = User.objects.create_user(username="user2", password="pass")
    user2.is_staff = True
    user2.save()

    # create a PENDING Order for user2 with quantity=1
    order2 = Order.objects.create(user=user2, status=Order.StatusChoices.PENDING)
    OrderItem.objects.create(
        order=order2,
        product=product,
        quantity=1,
        price=product.price,
        item_subtotal=product.price * 1,
    )

    client2 = APIClient()
    client2.force_authenticate(user=user2)

    # attempt checkout as user2 immediately → should be 400 (not enough free stock)
    resp2 = client2.post(url_checkout, {}, format="json")
    assert resp2.status_code == 400
    assert b"Not enough stock to reserve" in resp2.content

    # simulate the reservation expiring by setting reserved_until in the past
    past_time = timezone.now() - timedelta(seconds=1)
    Order.objects.filter(pk=order1.pk).update(reserved_until=past_time)

    # call the Celery task directly to release expired reservations
    from shop.tasks import release_expired_reservations

    release_expired_reservations()

    # after task runs, order1 should be CANCELLED and stock_reserved should return to 0
    order1.refresh_from_db()
    assert order1.status == Order.StatusChoices.CANCELLED
    product.refresh_from_db()
    assert product.stock_reserved == 0

    # now try checkout again as user2 → should succeed and reserve stock_reserved=1
    resp3 = client2.post(url_checkout, {}, format="json")
    assert resp3.status_code == 200
    order2.refresh_from_db()
    assert order2.status == Order.StatusChoices.AWAITING_PAYMENT
    product.refresh_from_db()
    assert product.stock_reserved == 1
