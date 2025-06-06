import base64

import pyotp
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django_otp.plugins.otp_totp.models import TOTPDevice
from djoser.signals import user_registered

from users.tasks import send_welcome_email


@receiver(pre_save, sender=TOTPDevice)
def ensure_base32_key(sender, instance, **kwargs):
    try:
        # try to decode the key as Base32
        base64.b32decode(instance.key, casefold=True)
    except Exception:
        # if decoding fails, generate a new random Base32 key
        instance.key = pyotp.random_base32()


# confirmation email after registration
@receiver(user_registered)
def on_user_registered(request, user, **kwargs):
    # sends an asynchronous welcome email via Celery
    send_welcome_email.delay(user.id)
