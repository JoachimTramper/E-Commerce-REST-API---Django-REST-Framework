import pytest
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework_simplejwt.tokens import RefreshToken


@pytest.mark.django_db
class Test2FAEnforcement:
    def test_access_without_2fa_header_fails(self, api_client, user):
        # simulate login
        token = RefreshToken.for_user(user).access_token
        api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        # ensure user has a confirmed device
        TOTPDevice.objects.create(user=user, confirmed=True)

        resp = api_client.get("/api/users/")  # any protected endpoint
        assert resp.status_code == 401
        assert "2FA token required" in str(resp.data)

    def test_access_with_invalid_2fa_header_fails(self, api_client, user):
        token = RefreshToken.for_user(user).access_token
        api_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}",
            HTTP_X_2FA_TOKEN="000000",
        )
        TOTPDevice.objects.create(user=user, confirmed=True)

        resp = api_client.get("/api/users/")
        assert resp.status_code == 401
        assert "Invalid 2FA token" in str(resp.data)

    def test_access_with_valid_2fa_header_succeeds(self, api_client, user):
        token = RefreshToken.for_user(user).access_token
        # setup a confirmed device and generate a valid code
        from pyotp import TOTP

        device = TOTPDevice.objects.create(user=user, confirmed=True)
        valid = TOTP(device.key).now()

        api_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token}",
            HTTP_X_2FA_TOKEN=valid,
        )
        resp = api_client.get("/api/users/")
        assert resp.status_code == 200
