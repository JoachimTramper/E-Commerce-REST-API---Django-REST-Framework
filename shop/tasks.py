from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from shop.models import Order


@shared_task
def send_order_confirmation_email(order_id):
    try:
        order = Order.objects.select_related("user").get(order_id=order_id)
    except Order.DoesNotExist:
        return f"Order {order_id} not found."

    subject = "Order Confirmation"
    message = (
        f"Hello {order.user.first_name},\n\n"
        f"Your order {order.order_number} has been confirmed.\n"
        f"Thank you for your purchase!"
    )
    recipient = [order.user.email]

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        recipient,
    )

    return f"Order confirmation sent for order {order_id}"
