from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string

User = get_user_model()


@shared_task
def send_welcome_email(user_id):
    # Fetch the user; exit early if not found
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return f"User {user_id} not found"

    # Prepare template context
    context = {
        "user": user,
        "domain": getattr(settings, "DEFAULT_DOMAIN", "example.com"),
        "protocol": getattr(settings, "DEFAULT_PROTOCOL", "https"),
    }

    subject = "Welcome to EcommerceAPI!"
    html_content = render_to_string("users/email/welcome_body.html", context)
    text_content = render_to_string("users/email/welcome.txt", context)

    # Obtain the default mail connection (respects settings.EMAIL_BACKEND)
    connection = get_connection()

    # Build multipart email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
        connection=connection,
    )
    email.attach_alternative(html_content, "text/html")

    # Send the email
    email.send(fail_silently=False)

    return f"Welcome email sent to {user.email}"
