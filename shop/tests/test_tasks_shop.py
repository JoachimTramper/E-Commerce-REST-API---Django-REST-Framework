import uuid
from datetime import timedelta

import pytest
from django.core import mail
from django.utils import timezone

from shop.models import Order
from shop.tasks import (
    _cancel_stale_pending_orders,
    cancel_stale_pending_orders,
    generate_order_report,
    send_daily_sales_report,
    send_order_email_with_invoice,
    send_pending_order_reminders,
)


@pytest.mark.django_db
class TestSendOrderEmailWithInvoice:
    def test_successful_invoice_email(self, order_factory):
        order = order_factory(status="confirmed")
        result = send_order_email_with_invoice(order.order_id)

        assert result.startswith("Order email with invoice sent")
        assert len(mail.outbox) == 1
        assert mail.outbox[0].to == [order.user.email]
        assert any(
            att[0] == f"invoice_{order.order_number}.pdf"
            for att in mail.outbox[0].attachments
        )

    def test_invalid_order_id(self):
        fake_uuid = uuid.uuid4()
        result = send_order_email_with_invoice(str(fake_uuid))
        assert result == f"Order {fake_uuid} not found."


@pytest.mark.django_db
class TestGenerateOrderReport:
    def test_successful_report(self, user_factory, order_factory):
        user = user_factory()
        order_factory(user=user, status="confirmed")

        result = generate_order_report(user.id)
        assert result == f"Order report sent to {user.email}"
        assert len(mail.outbox) == 1
        assert "orders.csv" in [att[0] for att in mail.outbox[0].attachments]

    def test_no_orders(self, user_factory):
        user = user_factory()
        result = generate_order_report(user.id)

        assert result == f"No orders found for user {user.email}"
        assert len(mail.outbox) == 0

    def test_invalid_user(self):
        result = generate_order_report(9999)
        assert result == "User 9999 not found."


@pytest.mark.django_db
class TestSendPendingOrderReminders:
    def test_one_hour_reminder(
        self, order_factory, order_item_factory, user_factory, product_factory
    ):
        user = user_factory(email="test@example.com")
        order = order_factory(
            user=user,
            status=Order.StatusChoices.PENDING,
            created_at=timezone.now() - timedelta(hours=1),
        )
        product = product_factory()
        order_item_factory(order=order, product=product, quantity=1)

        send_pending_order_reminders()

        assert len(mail.outbox) == 1

    def test_twelve_hour_reminder(self, order_factory):
        _ = order_factory(
            status=Order.StatusChoices.PENDING,
            created_at=timezone.now() - timedelta(hours=12),
        )

        send_pending_order_reminders()
        assert len(mail.outbox) == 1
        assert "Second Reminder" in mail.outbox[0].subject

    def test_timing_out_of_window(self, order_factory):
        _ = order_factory(
            status=Order.StatusChoices.PENDING,
            created_at=timezone.now() - timedelta(hours=2),
        )

        send_pending_order_reminders()
        assert len(mail.outbox) == 0


@pytest.mark.django_db
class TestCancelStalePendingOrders:
    def test_does_not_cancel_recent_order(self, order_factory):
        order = order_factory(
            status=Order.StatusChoices.PENDING,
            created_at=timezone.now() - timedelta(hours=23),
        )

        cancel_stale_pending_orders()
        order.refresh_from_db()
        assert order.status == Order.StatusChoices.PENDING
        assert len(mail.outbox) == 0

    def test_cancels_old_order(
        self, order_factory, order_item_factory, user_factory, product_factory
    ):
        user = user_factory(email="test@example.com")
        order = order_factory(
            user=user,
            status=Order.StatusChoices.PENDING,
            created_at=timezone.now() - timedelta(hours=25),
        )
        product = product_factory()
        order_item_factory(order=order, product=product, quantity=1)

        _cancel_stale_pending_orders()

        order.refresh_from_db()
        assert order.status == Order.StatusChoices.CANCELLED
        assert len(mail.outbox) == 1
        assert "cancelled" in mail.outbox[0].subject.lower()


@pytest.mark.django_db
class TestSendDailySalesReport:
    def test_sends_correct_email(
        self, order_factory, order_item_factory, user_factory, product_factory
    ):
        user = user_factory(email="admin@example.com")
        yesterday = timezone.now().replace(hour=10) - timedelta(days=1)

        product1 = product_factory(price=100)
        product2 = product_factory(price=50)

        order1 = order_factory(
            user=user, status=Order.StatusChoices.CONFIRMED, created_at=yesterday
        )
        order2 = order_factory(
            user=user, status=Order.StatusChoices.CANCELLED, created_at=yesterday
        )

        order_item_factory(order=order1, product=product1, quantity=1)
        order_item_factory(order=order2, product=product2, quantity=1)

        send_daily_sales_report()

        assert len(mail.outbox) == 1
        email = mail.outbox[0]
        assert "sales report" in email.subject.lower()
        assert "Total Orders" in email.body
        assert "€150.00" in email.body
        assert "Cancelled Orders: 1" in email.body


@pytest.mark.django_db
class TestPaymentWebhook:
    def test_payment_webhook_confirms_order(self, order_factory, client, settings):
        settings.WEBHOOK_SECRET_KEY = "testkey"
        order = order_factory(status=Order.StatusChoices.AWAITING_PAYMENT)

        response = client.post(
            "/api/webhooks/payment/",
            {"order_id": str(order.order_id), "status": "paid"},
            content_type="application/json",
            HTTP_X_WEBHOOK_KEY="testkey",  # correct key
        )

        order.refresh_from_db()
        assert response.status_code == 200
        assert order.status == Order.StatusChoices.CONFIRMED

    def test_invalid_webhook_key_is_rejected(self, order_factory, client, settings):
        settings.WEBHOOK_SECRET_KEY = "correct-key"
        order = order_factory(status=Order.StatusChoices.PENDING)

        response = client.post(
            "/api/webhooks/payment/",
            {"order_id": str(order.order_id), "status": "paid"},
            content_type="application/json",
            HTTP_X_WEBHOOK_KEY="wrong-key",  # wrong key
        )

        order.refresh_from_db()
        assert response.status_code == 403
        assert order.status == Order.StatusChoices.PENDING
