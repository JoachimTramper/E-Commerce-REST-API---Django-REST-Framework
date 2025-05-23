import csv
import io

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import localtime
from xhtml2pdf import pisa

from shop.models import Order


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
                localtime(order.created_at).strftime("%Y-%m-%d %H:%M"),
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

    # Render PDF from template
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
