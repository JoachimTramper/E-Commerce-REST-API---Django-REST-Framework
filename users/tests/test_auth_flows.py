import re
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

User = get_user_model()


@pytest.mark.django_db
class TestAuthFlows:
    def test_me_endpoint(self, auth_client):
        # GET /api/auth/users/me/
        resp = auth_client.get("/api/auth/users/me/")
        assert resp.status_code == 200, f"Me endpoint failed: {resp.data}"
        assert resp.data.get("email") == "foo@bar.com"

    def test_jwt_login_and_refresh(self, api_client, user):
        # login and obtain JWT tokens
        resp = api_client.post(
            "/api/auth/jwt/create/",
            {"email": user.email, "password": "UncommonP4ssw0rd!"},
            format="json",
        )
        assert resp.status_code == 200, f"Login failed: {resp.data}"
        assert "access" in resp.data and "refresh" in resp.data
        refresh = resp.data["refresh"]

        # access token refresh
        resp = api_client.post(
            "/api/auth/jwt/refresh/", {"refresh": refresh}, format="json"
        )
        assert resp.status_code == 200, f"Token refresh failed: {resp.data}"
        assert "access" in resp.data

    @patch("users.tasks.send_welcome_email.delay")
    def test_registration_and_activation(
        self, mock_send_welcome_email_delay, api_client, mailoutbox
    ):
        url = reverse("user-list")
        payload = {
            "email": "foo@bar.com",
            "username": "foobar",
            "password": "UncommonP4ssw0rd!",
            "re_password": "UncommonP4ssw0rd!",
        }

        resp = api_client.post(url, payload, format="json")
        assert resp.status_code == 201

        # check activation email was sent
        assert len(mailoutbox) == 1
        assert any("activate/" in m.body for m in mailoutbox)

        # get uid and token from activation email
        email_body = next(m.body for m in mailoutbox if "activate/" in m.body)
        match = re.search(r"activate/(?P<uid>[^/]+)/(?P<token>[^/]+)", email_body)
        assert match
        uid, token = match.group("uid", "token")

        # acctivate user via API
        activation_url = reverse("user-activation")
        resp2 = api_client.post(
            activation_url, {"uid": uid, "token": token}, format="json"
        )
        assert resp2.status_code == 204

        user = User.objects.get(username="foobar")
        mock_send_welcome_email_delay.assert_called_once_with(user.id)

    def test_password_reset_flow(self, api_client, mailoutbox, user):
        # request reset email
        resp = api_client.post(
            "/api/auth/users/reset_password/", {"email": user.email}, format="json"
        )
        assert resp.status_code == 204
        assert len(mailoutbox) == 1

        # generate fresh uid & token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # confirm reset
        new_pw = "NewStr0ngP@ss!"
        resp = api_client.post(
            "/api/auth/users/reset_password_confirm/",
            {
                "uid": uid,
                "token": token,
                "new_password": new_pw,
                "re_new_password": new_pw,
            },
            format="json",
        )
        assert resp.status_code == 204

        # verify login with new password
        resp = api_client.post(
            "/api/auth/jwt/create/",
            {"email": user.email, "password": new_pw},
            format="json",
        )
        assert resp.status_code == 200
        assert "access" in resp.data and "refresh" in resp.data
