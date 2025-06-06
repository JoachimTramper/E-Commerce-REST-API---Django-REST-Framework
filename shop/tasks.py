import csv
import io
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, send_mail
from django.db import transaction
from django.db.models import F
from django.template.loader import render_to_string
from django.utils import timezone
from xhtml2pdf import pisa

from shop.models import Order, Product


@shared_task
def generate_order_report(user_id):
    User = get_user_model()
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return f"User {user_id} not found."

    orders = (
        Order.objects.filter(user=user)
        .select_related("user")
        .prefetch_related("items__product")
    )

    if not orders.exists():
        return f"No orders found for user {user.email}"

    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["Order Number", "Status", "Created At", "Total Items"])

    for order in orders:
        writer.writerow(
            [
                order.order_number,
                order.status,
                timezone.localtime(order.created_at).strftime("%Y-%m-%d %H:%M"),
                order.items.count(),
            ]
        )

    buffer.seek(0)
    email = EmailMessage(
        subject="Your Order Report",
        body=f"Hello {user.first_name},\n\nFind attached your order report.",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    email.attach("orders.csv", buffer.getvalue(), "text/csv")
    email.send()

    return f"Order report sent to {user.email}"


@shared_task
def send_order_email_with_invoice(order_id):
    try:
        order = (
            Order.objects.select_related("user")
            .prefetch_related("items__product")
            .get(order_id=order_id)
        )
    except Order.DoesNotExist:
        return f"Order {order_id} not found."

    # render PDF from template
    html = render_to_string("shop/invoice.html", {"order": order})
    buffer = io.BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=buffer)

    if pisa_status.err:
        return f"PDF generation failed for order {order_id}"

    buffer.seek(0)

    # Compose email
    subject = f"Your Order #{order.order_number} Confirmation & Invoice"
    message = (
        f"Hello {order.user.first_name},\n\n"
        f"Thank you for your order #{order.order_number}.\n"
        f"Please find your invoice attached.\n\n"
        f"Kind regards,\n"
        f"The Team"
    )
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[order.user.email],
    )
    email.attach("invoice.pdf", buffer.read(), "application/pdf")
    email.send()

    return f"Order email with invoice sent for order {order_id}"


@shared_task
def send_pending_order_reminders():
    now = timezone.now()

    orders = Order.objects.filter(status=Order.StatusChoices.PENDING)

    for order in orders:
        elapsed = timezone.now() - order.created_at
        print(
            f"[REMINDER] Order {order.order_number}: created_at={order.created_at}, "
            f"elapsed={elapsed}"
        )
        email = order.user.email
        name = order.user.first_name
        order_num = order.order_number
        created_at = order.created_at
        time_since = now - created_at

        if abs(time_since - timedelta(hours=1)) < timedelta(minutes=5):
            send_mail(
                f"Reminder: Complete Your Order #{order_num}",
                f"Hi {name},\n\n"
                "Just a quick reminder that your order is still waiting for you!\n\n"
                "Kind regards,\nTeam",
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )
        elif abs(time_since - timedelta(hours=12)) < timedelta(minutes=5):
            send_mail(
                f"Second Reminder: Order #{order_num} Still Pending",
                f"Hi {name},\n\n"
                "We're holding your order for a bit longer. Want to finish checking out?\n\n"
                "Team",
                settings.DEFAULT_FROM_EMAIL,
                [email],
            )


def _cancel_stale_pending_orders():
    now = timezone.now()
    cutoff = now - timedelta(hours=24)

    stale_orders = Order.objects.filter(
        status=Order.StatusChoices.PENDING, created_at__lt=cutoff
    )

    for order in stale_orders:
        order.status = Order.StatusChoices.CANCELLED
        order.save()

        send_mail(
            f"Order #{order.order_number} Cancelled",
            f"Hi {order.user.first_name},\n\n"
            "We’ve cancelled your order as it wasn’t completed within 24 hours.\n\n"
            "Team",
            settings.DEFAULT_FROM_EMAIL,
            [order.user.email],
        )

    return f"{stale_orders.count()} pending orders cancelled."


# bypassing _cancel_stale_pending_orders to avoid deleting orders in DEBUG mode
@shared_task
def cancel_stale_pending_orders():
    if not settings.DEBUG:
        return _cancel_stale_pending_orders()
    return "Skipping auto-cancellation in DEBUG mode"


@shared_task
def send_daily_sales_report():
    start = timezone.now().replace(
        hour=0, minute=0, second=0, microsecond=0
    ) - timedelta(days=1)
    end = start + timedelta(days=1)

    orders = Order.objects.filter(created_at__range=(start, end))
    total_orders = orders.count()
    total_revenue = sum(order.total_amount for order in orders)
    cancelled_orders = orders.filter(status=Order.StatusChoices.CANCELLED).count()

    message = (
        f"🛒 Daily Sales Report ({start.date()}):\n\n"
        f"- Total Orders: {total_orders}\n"
        f"- Total Revenue: €{total_revenue:.2f}\n"
        f"- Cancelled Orders: {cancelled_orders}\n"
    )

    email = EmailMessage(
        subject=f"Daily Sales Report – {start.date()}",
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=["admin@shop.com"],
    )
    email.send()

    return f"Sales report sent for {start.date()}"


@shared_task
def release_expired_reservations():
    now = timezone.now()
    expired_orders = Order.objects.filter(
        status=Order.StatusChoices.AWAITING_PAYMENT, reserved_until__lt=now
    )

    for order in expired_orders:
        with transaction.atomic():
            for item in order.items.all():
                Product.objects.filter(pk=item.product_id).update(
                    stock_reserved=F("stock_reserved") - item.quantity
                )
            order.status = Order.StatusChoices.CANCELLED
            order.save()
