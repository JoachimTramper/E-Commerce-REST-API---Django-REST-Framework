import pytest
from django.contrib.auth import get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
class TestCustomTokenObtainPairView:
    endpoint = "/api/users/auth/jwt/create/"

    def test_has_2fa_false_when_no_device(self, user):
        """
        If user has no confirmed TOTPDevice, has_2fa must be False.
        """
        client = APIClient()
        resp = client.post(
            self.endpoint,
            {"email": user.email, "password": "UncommonP4ssw0rd!"},
            format="json",
        )
        assert resp.status_code == 200
        assert resp.data["has_2fa"] is False

    def test_has_2fa_true_when_device_exists(self, user):
        """
        If user has at least one confirmed TOTPDevice, has_2fa must be True.
        """
        TOTPDevice.objects.create(user=user, confirmed=True)
        client = APIClient()
        resp = client.post(
            self.endpoint,
            {"email": user.email, "password": "UncommonP4ssw0rd!"},
            format="json",
        )
        assert resp.status_code == 200
        assert resp.data["has_2fa"] is True
