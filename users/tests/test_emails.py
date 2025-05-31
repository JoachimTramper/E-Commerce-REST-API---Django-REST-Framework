import re

import pytest
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from djoser.email import ActivationEmail


@pytest.mark.django_db
def test_registration_sends_welcome_and_activation_mail(api_client, mailoutbox):
    payload = {
        "email": "foo@bar.com",
        "username": "foobar",
        "password": "UncommonP4ssw0rd!",
        "re_password": "UncommonP4ssw0rd!",
    }
    resp = api_client.post(reverse("user-list"), payload, format="json")
    assert resp.status_code == 201, f"Registration failed: {resp.data}"

    # check that at least 2 emails were sent (activation + welcome)
    assert (
        len(mailoutbox) >= 2
    ), f"Expected activation + welcome emails, but got: {len(mailoutbox)}"

    # find the activation email and check its custom subject
    activation_email = next(
        m
        for m in mailoutbox
        if isinstance(m, ActivationEmail) or "activate/" in getattr(m, "body", "")
    )
    assert "Activate your EcommerceAPI account" in activation_email.subject

    # find the welcome email and check its custom subject
    welcome_email = next(
        m for m in mailoutbox if "Welcome to EcommerceAPI!" in m.subject
    )
    assert (
        welcome_email is not None
    ), f"No welcome email found, subjects: {[m.subject for m in mailoutbox]}"


@pytest.mark.django_db
def test_user_can_activate_account(api_client, mailoutbox):
    # register another user to get a fresh activation link
    payload = {
        "email": "bar@foo.com",
        "username": "barfoo",
        "password": "AnotherP4ssw0rd!",
        "re_password": "AnotherP4ssw0rd!",
    }
    resp = api_client.post(reverse("user-list"), payload, format="json")
    assert resp.status_code == 201

    # find the activation email in mailoutbox
    activation_email = next(
        m
        for m in mailoutbox
        if isinstance(m, ActivationEmail) or "activate/" in getattr(m, "body", "")
    )
    email_body = activation_email.body

    # extract uid and token from the activation link
    match = re.search(r"activate/(?P<uid>[^/]+)/(?P<token>[^/]+)", email_body)
    assert match, "Activation link not found in activation email"
    uid_from_link, token_from_link = match.group("uid", "token")

    # retrieve the user from activation_email.context and generate valid uid & token
    user = activation_email.context["user"]
    uid_bytes = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)

    # activate the account using the activation endpoint
    activation_url = reverse("user-activation")
    resp2 = api_client.post(
        activation_url, {"uid": uid_bytes, "token": token}, format="json"
    )
    assert resp2.status_code == 204, f"Activation failed: {resp2.data}"


@pytest.mark.django_db
def test_password_reset_email_uses_custom_template(api_client, user, mailoutbox):
    # trigger password reset email
    resp = api_client.post(
        "/api/auth/users/reset_password/",
        {"email": user.email},
        format="json",
    )
    assert resp.status_code == 204

    # exactly one reset email should be sent
    assert len(mailoutbox) == 1, f"Expected 1 reset email, got {len(mailoutbox)}"
    email = mailoutbox[0]

    # check custom subject and plain-text body
    assert "Reset your EcommerceAPI password" in email.subject
    assert "You requested a password reset." in email.body

    # check reset link format in body
    assert re.search(
        r"password/reset/confirm/[^/]+/[^/]+", email.body
    ), "Reset link format incorrect"
