import pyotp
import pytest
from django_otp.plugins.otp_totp.models import TOTPDevice


@pytest.mark.django_db
class TestTOTP2FABasic:
    def test_unauthenticated_cannot_access_setup(self, api_client):
        resp = api_client.get("/api/users/2fa/setup/")
        assert resp.status_code == 401

    def test_setup_returns_qr_and_secret(self, auth_client, user):
        resp = auth_client.get("/api/users/2fa/setup/")
        assert resp.status_code == 200
        data = resp.data
        assert "qr_code" in data and isinstance(data["qr_code"], str)
        assert "secret" in data and isinstance(data["secret"], str)

        # Exactly one unconfirmed device should exist
        devices = TOTPDevice.objects.filter(user=user, confirmed=False)
        assert devices.count() == 1

    def test_verify_invalid_token(self, auth_client):
        auth_client.get("/api/users/2fa/setup/")
        resp = auth_client.post("/api/users/2fa/verify/", {"token": "000000"})
        assert resp.status_code == 400
        assert "token" in resp.data

    def test_full_2fa_flow_and_disable(self, auth_client, user):
        setup = auth_client.get("/api/users/2fa/setup/").data
        secret = setup["secret"]

        valid_token = pyotp.TOTP(secret).now()
        resp = auth_client.post("/api/users/2fa/verify/", {"token": valid_token})
        assert resp.status_code == 204

        # Confirmed device exists
        confirmed = TOTPDevice.objects.filter(user=user, confirmed=True)
        assert confirmed.count() == 1

        # Disable all 2FA
        resp = auth_client.delete("/api/users/2fa/")
        assert resp.status_code == 204
        assert TOTPDevice.objects.filter(user=user).count() == 0


@pytest.mark.django_db
class TestTOTP2FAEdgeCases:
    def test_unauthenticated_cannot_verify_or_disable(self, api_client):
        resp1 = api_client.post("/api/users/2fa/verify/", {"token": "123456"})
        assert resp1.status_code == 401

        resp2 = api_client.delete("/api/users/2fa/")
        assert resp2.status_code == 401

    def test_double_setup_deletes_unconfirmed(self, auth_client, user):
        # First setup
        auth_client.get("/api/users/2fa/setup/")
        # Create a second unconfirmed device
        auth_client.get("/api/users/2fa/setup/")

        unconfirmed = TOTPDevice.objects.filter(user=user, confirmed=False)
        assert unconfirmed.count() == 1

    def test_verify_without_setup(self, auth_client):
        resp = auth_client.post("/api/users/2fa/verify/", {"token": "123456"})
        assert resp.status_code == 400
        assert "No setup in progress" in str(resp.data)

    def test_disable_after_disable(self, auth_client, user):
        # Setup & verify to create a confirmed device
        setup = auth_client.get("/api/users/2fa/setup/").data
        secret = setup["secret"]
        valid = pyotp.TOTP(secret).now()
        auth_client.post("/api/users/2fa/verify/", {"token": valid})

        # First disable
        resp1 = auth_client.delete("/api/users/2fa/")
        assert resp1.status_code == 204

        # Second disable should still return 204 and leave zero devices
        resp2 = auth_client.delete("/api/users/2fa/")
        assert resp2.status_code == 204
        assert TOTPDevice.objects.filter(user=user).count() == 0

    def test_confirmed_device_survives_setup(self, auth_client, user):
        # Setup & verify first device
        setup = auth_client.get("/api/users/2fa/setup/").data
        secret1 = setup["secret"]
        valid1 = pyotp.TOTP(secret1).now()
        auth_client.post("/api/users/2fa/verify/", {"token": valid1})

        # Another setup: should only delete unconfirmed devices
        auth_client.get("/api/users/2fa/setup/")

        confirmed = TOTPDevice.objects.filter(user=user, confirmed=True)
        assert confirmed.count() == 1
