import re

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_activation_email_uses_custom_template(api_client, mailoutbox):
    # Register a new user
    payload = {
        "email": "new@user.com",
        "username": "newuser",
        "password": "Test1234!",
        "re_password": "Test1234!",
    }
    resp = api_client.post(reverse("user-list"), payload, format="json")
    assert resp.status_code == 201

    # Exactly one activation email should be sent
    assert len(mailoutbox) == 1
    email = mailoutbox[0]

    # Check custom subject and plain‐text body
    assert "Activate your EcommerceAPI account" in email.subject
    assert "Welcome to EcommerceAPI!" in email.body

    # Check activation link format in body
    assert re.search(r"activate/[^/]+/[^/]+", email.body)


@pytest.mark.django_db
def test_password_reset_email_uses_custom_template(api_client, user, mailoutbox):
    # Trigger password reset email
    resp = api_client.post(
        "/api/auth/users/reset_password/",
        {"email": user.email},
        format="json",
    )
    assert resp.status_code == 204

    # Exactly one reset email should be sent
    assert len(mailoutbox) == 1
    email = mailoutbox[0]

    # Check custom subject and plain‐text body
    assert "Reset your EcommerceAPI password" in email.subject
    assert "You requested a password reset." in email.body

    # Check reset link format in body
    assert re.search(r"password/reset/confirm/[^/]+/[^/]+", email.body)
