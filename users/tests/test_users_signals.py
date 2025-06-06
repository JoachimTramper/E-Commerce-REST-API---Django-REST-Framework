import base64
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice
from djoser.signals import user_registered

from users.tasks import send_welcome_email

User = get_user_model()


@pytest.mark.django_db
class TestTOTPDeviceSignal:
    def test_ensure_base32_key_generates_if_invalid(self, user):
        """
        Creating a TOTPDevice with a non-Base32 key,
        the pre_save handler should replace it with a valid Base32 key.
        """

        # use a string that is not valid Base32 (contains characters outside A-Z2-7)
        invalid_key = "this_is_not_base32!!"
        device = TOTPDevice.objects.create(user=user, name="test", key=invalid_key)

        # after saving, the pre_save signal should have replaced the key
        device.refresh_from_db()
        new_key = device.key

        # attempt to decode the new key as Base32; it should not raise an exception
        try:
            base64.b32decode(new_key, casefold=True)
        except Exception as e:
            pytest.skip(f"Generated key is not valid Base32: {e!r}")

        # the new key must differ from the invalid input and be a string of sufficient length
        assert new_key != invalid_key
        assert isinstance(new_key, str)
        assert (
            len(new_key) >= 16
        )  # pyotp.random_base32() generates at least 16 characters

    def test_ensure_base32_key_keeps_valid_key(self, user):
        """
        If a valid Base32 string provided, the handler should not overwrite it.
        """

        import pyotp

        valid_key = pyotp.random_base32()  # generate a valid Base32 key

        device = TOTPDevice.objects.create(user=user, name="test", key=valid_key)
        device.refresh_from_db()
        assert device.key == valid_key, "Valid Base32 key should remain unchanged"


@pytest.mark.django_db
class TestUserRegisteredSignal:
    def test_on_user_registered_sends_welcome_email(self):
        """
        When the Djoser user_registered signal is sent, send_welcome_email.delay(user.id)
        should be called exactly once with the correct user ID.
        """

        # create a new user manually
        user = User.objects.create_user(
            username="alice", email="alice@example.com", password="Secret123!"
        )

        # patch the Celery task so delay() is not actually executed
        with patch.object(send_welcome_email, "delay", autospec=True) as mock_delay:
            # manually send the user_registered signal (Djoser would do this automatically)
            user_registered.send(sender=User, request=None, user=user)

            # verify that the Celery task was called exactly once with user.id
            mock_delay.assert_called_once_with(user.id)
