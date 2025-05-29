import pytest


@pytest.mark.django_db
class TestMeProfileEndpoints:
    endpoint = "/api/users/me/profile/"

    def test_get_me_profile(self, auth_client, profile):
        response = auth_client.get(self.endpoint)
        assert response.status_code == 200
        data = response.json()
        # check if the profile data matches
        assert data["id"] == profile.id
        assert "phone_number" in data

    def test_patch_me_profile(self, auth_client, profile):
        payload = {"phone_number": "0123456789"}
        response = auth_client.patch(self.endpoint, payload)
        assert response.status_code == 200
        data = response.json()
        assert data["phone_number"] == "0123456789"
        # check if the profile was updated in the database
        profile.refresh_from_db()
        assert profile.phone_number == "0123456789"

    def test_unauthenticated_cannot_get(self, api_client):
        response = api_client.get(self.endpoint)
        assert response.status_code == 401

    def test_unauthenticated_cannot_patch(self, api_client):
        response = api_client.patch(self.endpoint, {"phone_number": "000"})
        assert response.status_code == 401


@pytest.mark.django_db
class TestMeDelete:
    def test_user_can_soft_delete_own_account(self, auth_client, user):
        # Before: user is active
        assert user.is_active is True

        response = auth_client.delete("/api/users/me/delete/")
        assert response.status_code == 204

        # After: user still exists, but is inactive
        user.refresh_from_db()
        assert user.is_active is False

    def test_unauthenticated_cannot_delete(self, api_client):
        response = api_client.delete("/api/users/me/delete/")
        assert response.status_code == 401


@pytest.mark.django_db
class TestAdminProfileAccess:
    def test_admin_can_list_profiles(self, admin_client, profile):
        response = admin_client.get("/api/users/profiles/")
        assert response.status_code == 200
        payload = response.json()
        assert payload["count"] >= 1
        assert any(
            p["phone_number"] == profile.phone_number for p in payload["results"]
        )

    def test_admin_can_patch_profile(self, admin_client, profile):
        url = f"/api/users/profiles/{profile.id}/"
        response = admin_client.patch(url, {"phone_number": "0987654321"})
        assert response.status_code == 200
        assert response.json()["phone_number"] == "0987654321"

    def test_admin_can_create_profile_for_user(self, admin_client, user):
        payload = {
            "user": user.id,
            "phone_number": "0611223344",
            "date_of_birth": "1990-01-01",
        }
        response = admin_client.post("/api/users/profiles/", payload)
        assert response.status_code == 201
        assert response.json()["user"] == user.id


@pytest.mark.django_db
class TestUserCannotAccessOthersProfiles:
    def test_user_cannot_list_profiles(self, auth_client):
        response = auth_client.get("/api/users/profiles/")
        assert response.status_code == 403

    def test_user_cannot_access_other_profile(self, auth_client, profile):
        url = f"/api/users/profiles/{profile.id}/"
        response = auth_client.get(url)
        assert response.status_code == 403
