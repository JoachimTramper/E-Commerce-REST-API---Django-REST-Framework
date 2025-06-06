import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistrationValidation:
    def test_invalid_email_format_returns_400(self, api_client):
        payload = {
            "email": "not-an-email",
            "username": "testuser",
            "password": "ValidP4ssw0rd!",
            "re_password": "ValidP4ssw0rd!",
        }
        resp = api_client.post(reverse("user-list"), payload, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        # expect "Enter a valid email address." or similar in the response
        assert "email" in resp.data
        assert any("valid email" in str(msg).lower() for msg in resp.data["email"])

    def test_weak_password_returns_400(self, api_client):
        payload = {
            "email": "foo@example.com",
            "username": "weakpassuser",
            "password": "123",  # too short / purely numeric
            "re_password": "123",
        }
        resp = api_client.post(reverse("user-list"), payload, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        # Expect an error on “password” field indicating weakness
        assert "password" in resp.data
        assert any("password" in str(msg).lower() for msg in resp.data["password"])


@pytest.mark.django_db
class TestUserPartialUpdateValidation:
    def test_patch_user_invalid_email_format_returns_400(self, auth_client, user):
        client = auth_client
        client.force_authenticate(user)

        resp = client.patch(
            reverse("user-me"), {"email": "not-an-email"}, format="json"
        )
        print("DEBUG: invalid-email test")
        print("  Status code:", resp.status_code)
        print("  resp.data:", resp.data)
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in resp.data
        assert any("valid email" in str(msg).lower() for msg in resp.data["email"])

    def test_patch_user_valid_email_updates(self, auth_client, user):
        client = auth_client
        client.force_authenticate(user)

        new_email = "new@example.com"
        resp = client.patch(reverse("user-me"), {"email": new_email}, format="json")
        print("DEBUG: invalid-email test")
        print("  Status code:", resp.status_code)
        print("  resp.data:", resp.data)
        assert resp.status_code == status.HTTP_200_OK

        user.refresh_from_db()
        assert user.email == new_email

    def test_patch_user_cannot_remove_required_fields(self, auth_client, user):
        """
        PATCH /users/me/ with an empty payload (no changes) should still succeed (HTTP 200),
        but PATCH with blank username should return 400.
        """
        client = auth_client
        client.force_authenticate(user)

        # empty PATCH is acceptable (no error) → returns HTTP 200 and no changes
        resp_empty = client.patch(reverse("user-me"), {}, format="json")
        assert resp_empty.status_code == status.HTTP_200_OK

        # trying to clear username (blank string) should be invalid
        resp_blank = client.patch(reverse("user-me"), {"username": ""}, format="json")
        assert resp_blank.status_code == status.HTTP_400_BAD_REQUEST
        assert "username" in resp_blank.data
        assert any(
            "blank" in str(msg).lower() or "required" in str(msg).lower()
            for msg in resp_blank.data["username"]
        )


@pytest.mark.django_db
class TestAddressValidation:
    def test_create_address_invalid_postal_code_returns_400(self, auth_client, user):
        client = auth_client
        client.force_authenticate(user)

        payload = {
            "label": "Home",
            "street": "Example St",
            "number": "10A",
            "zipcode": "12",  # invalid postal code, too short
            "city": "Amsterdam",
            "country": "Netherlands",
            "is_billing": True,
            "is_shipping": True,
        }
        resp = client.post(reverse("users:me-addresses"), payload, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "zipcode" in resp.data
        assert any(
            "postal" in str(msg).lower() or "zip" in str(msg).lower()
            for msg in resp.data["zipcode"]
        )

    def test_patch_address_invalid_phone_returns_400(self, auth_client, address):
        client = auth_client
        client.force_authenticate(address.profile.user)

        invalid_payload = {"phone_number": "not-a-phone-number"}
        resp = client.patch(
            reverse("users:me-profile"),
            invalid_payload,
            format="json",
        )
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "phone_number" in resp.data
        assert any("numeric" in str(msg).lower() for msg in resp.data["phone_number"])
