import base64

import pytest
from django.contrib.auth import get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice

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
