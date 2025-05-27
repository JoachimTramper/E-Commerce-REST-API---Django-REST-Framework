from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"

    def ready(self):
        # Load signal handlers (pre_save Base32 fixer)  # noqa: F401
        import base64  # noqa: F401

        # Monkey-patch bin_key: try hex first, else Base32
        import binascii

        from django_otp.plugins.otp_totp.models import TOTPDevice

        import users.signals  # noqa: F401

        def patched_bin_key(self):
            key_bytes = (self.key or "").encode()
            try:
                # first assume hex
                return binascii.unhexlify(key_bytes)
            except binascii.Error:
                # fallback to Base32
                return base64.b32decode(key_bytes, casefold=True)

        TOTPDevice.bin_key = property(patched_bin_key)
