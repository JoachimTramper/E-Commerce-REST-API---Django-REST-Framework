import re

import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestUserEmailFlows:
    @pytest.fixture(autouse=True)
    def enable_celery_eager(self, settings):
        # run Celery tasks synchronously in tests
        settings.CELERY_TASK_ALWAYS_EAGER = True
        settings.CELERY_TASK_EAGER_PROPAGATES = True

    def test_welcome_mail_sent_after_registration(self, api_client, mailoutbox):
        """
        After registering a new user we expect:
         1) the Djoser activation email
         2) our custom welcome email via Celery
        """
        payload = {
            "email": "new@user.com",
            "username": "newuser",
            "password": "Test1234!",
            "re_password": "Test1234!",
        }
        resp = api_client.post(reverse("user-list"), payload, format="json")
        assert resp.status_code == 201

        # exactly two emails should be sent
        assert len(mailoutbox) == 2

        # one of them must be our welcome mail
        assert any("Welcome to EcommerceAPI!" in m.subject for m in mailoutbox)

    def test_password_change_confirmation_mail_sent(self, api_client, user, mailoutbox):
        """
        After confirming a password reset we expect:
         1) the Djoser reset-link email
         2) the Djoser password-changed confirmation email
        """
        # 1) trigger reset-link email
        reset_url = reverse("user-reset-password")
        resp = api_client.post(reset_url, {"email": user.email}, format="json")
        assert resp.status_code == 204
        assert len(mailoutbox) == 1

        # extract uid & token from that email
        body = mailoutbox[0].body
        match = re.search(r"password/reset/confirm/([^/]+)/([^/\s]+)", body)
        assert match, "No reset-confirm link found in email"
        uid, token = match.groups()
        token = token.strip()

        # confirm the reset with both password fields as Djoser expects
        confirm_url = reverse("user-reset-password-confirm")
        payload = {
            "uid": uid,
            "token": token,
            "new_password": "NewP4ssw0rd!",
            "re_new_password": "NewP4ssw0rd!",
        }
        resp2 = api_client.post(confirm_url, payload, format="json")
        assert resp2.status_code == 204

        # now two emails: reset-link + confirmation
        assert len(mailoutbox) == 2
        assert any(
            "password has been successfully changed" in m.subject for m in mailoutbox
        ), f"Unexpected subjects: {[m.subject for m in mailoutbox]}"
