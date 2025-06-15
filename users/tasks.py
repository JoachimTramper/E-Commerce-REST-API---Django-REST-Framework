from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.template.loader import render_to_string

User = get_user_model()


@shared_task
def send_welcome_email(user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return f"User {user_id} not found"

    current_site = Site.objects.get_current()
    domain = current_site.domain
    protocol = "https"

    context = {
        "user": user,
        "domain": domain,
        "protocol": protocol,
    }

    subject = "Welcome to EcommerceAPI!"
    message = render_to_string("users/email/welcome.html", context)

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=message,
    )
    return f"Welcome email sent to {user.email}"
