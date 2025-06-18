from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string

User = get_user_model()


@shared_task
def send_welcome_email(user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return f"User {user_id} not found"

    context = {
        "user": user,
        "domain": settings.DEFAULT_DOMAIN,
        "protocol": settings.DEFAULT_PROTOCOL,
    }

    domain = getattr(settings, "DEFAULT_DOMAIN", "example.com")
    protocol = getattr(settings, "DEFAULT_PROTOCOL", "https")
    context = {
        "user": user,
        "domain": domain,
        "protocol": protocol,
    }

    subject = "Welcome to EcommerceAPI!"
    html_message = render_to_string("users/email/welcome.html", context)
    text_message = render_to_string("users/email/welcome.txt", context)

    send_mail(
        subject,
        text_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
    )
    return f"Welcome email sent to {user.email}"
