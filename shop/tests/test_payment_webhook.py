import uuid
from unittest.mock import patch

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from shop.models import Order, OrderItem
from shop.tasks import send_order_email_with_invoice


@pytest.mark.django_db
class TestPaymentWebhook:
    def test_payment_webhook_marks_order_confirmed(
        self, admin_client, settings, user, product_factory, order_factory
    ):
        # create product
        product = product_factory()

        # create order with status "awaiting payment", then attach an OrderItem
        order = order_factory(user=user, status=Order.StatusChoices.AWAITING_PAYMENT)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            price=product.price,
        )

        # prepare payload
        payload = {
            "order_id": order.order_id,
            "status": "paid",
        }
        # fetch url
        url = reverse("payment-webhook")

        # include the X-Webhook-Key header; in the DRF test client, it's set as HTTP_X_WEBHOOK_KEY.
        secret = settings.WEBHOOK_SECRET_KEY
        resp = admin_client.post(
            url,
            payload,
            format="json",
            HTTP_X_WEBHOOK_KEY=secret,
        )

        assert resp.status_code == status.HTTP_200_OK

        # check if order status is updated to "confirmed"
        order.refresh_from_db()
        assert order.status == Order.StatusChoices.CONFIRMED

    def test_payment_webhook_with_nonexistent_order_id(self, admin_client, settings):
        fake_order_id = uuid.uuid4()

        payload = {
            "order_id": fake_order_id,
            "status": "paid",
        }
        url = reverse("payment-webhook")

        # include the correct webhook secret header
        secret = settings.WEBHOOK_SECRET_KEY
        resp = admin_client.post(
            url,
            payload,
            format="json",
            HTTP_X_WEBHOOK_KEY=secret,
        )

        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_payment_webhook_with_failed_status_does_not_update_order(
        self, admin_client, user, product_factory, order_factory, settings
    ):
        # create a product and an order with status "Pending"
        product = product_factory()
        order = order_factory(user=user, status=Order.StatusChoices.PENDING)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            price=product.price,
        )

        # simulate the webhook payload with status="failed"
        payload = {
            "order_id": order.order_id,
            "status": "failed",
        }
        url = reverse("payment-webhook")
        secret = settings.WEBHOOK_SECRET_KEY
        resp = admin_client.post(
            url,
            payload,
            format="json",
            HTTP_X_WEBHOOK_KEY=secret,
        )

        assert resp.status_code == status.HTTP_200_OK

        order.refresh_from_db()
        assert order.status == Order.StatusChoices.PENDING

    def test_webhook_triggers_invoice_email(
        self, user, product_factory, order_factory, settings
    ):
        """
        Verify that when the payment webhook posts status="paid" for an
        order in AWAITING_PAYMENT, the order is marked CONFIRMED and
        send_order_email_with_invoice.delay() is called with the correct order_id.
        """

        # set the expected webhook header key
        settings.WEBHOOK_SECRET_KEY = "secret123"

        # create a product (so OrderItem can reference it) and an order in AWAITING_PAYMENT
        product = product_factory(stock=5)
        order = order_factory(user=user, status=Order.StatusChoices.AWAITING_PAYMENT)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=2,
            price=product.price,
            item_subtotal=product.price * 2,
        )

        # patch the Celery task send_order_email_with_invoice.delay
        with patch.object(send_order_email_with_invoice, "delay") as mock_delay:
            client = APIClient()

            # prepare headers and payload for the webhook endpoint
            headers = {"HTTP_X_WEBHOOK_KEY": "secret123"}
            payload = {"order_id": str(order.order_id), "status": "paid"}

            # call the payment webhook
            url = reverse("payment-webhook")
            resp = client.post(url, payload, format="json", **headers)
            assert resp.status_code == status.HTTP_200_OK

            # after webhook, the order status should be CONFIRMED
            order.refresh_from_db()
            assert order.status == Order.StatusChoices.CONFIRMED

            # confirm that send_order_email_with_invoice.delay was called once
            mock_delay.assert_called_once_with(str(order.order_id))
