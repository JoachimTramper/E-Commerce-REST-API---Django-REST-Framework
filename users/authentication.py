from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication


class TwoFactorJWTAuthentication(JWTAuthentication):
    """
    Extend JWT auth: if user has confirmed TOTPDevice(s), require
    one-time token in X-2FA-Token header on each request.
    """

    def authenticate(self, request):
        # Normal JWT authentication first
        user_auth_tuple = super().authenticate(request)
        if user_auth_tuple is None:
            return None

        user, validated_token = user_auth_tuple

        # If user has confirmed 2FA devices, enforce TOTP
        if TOTPDevice.objects.filter(user=user, confirmed=True).exists():
            token = request.headers.get("X-2FA-Token")
            if not token:
                raise exceptions.AuthenticationFailed(
                    "2FA token required", code="2fa_required"
                )

            # Verify against any of the user's devices
            devices = TOTPDevice.objects.filter(user=user, confirmed=True)
            if not any(device.verify_token(token) for device in devices):
                raise exceptions.AuthenticationFailed(
                    "Invalid 2FA token", code="2fa_invalid"
                )

        return (user, validated_token)
