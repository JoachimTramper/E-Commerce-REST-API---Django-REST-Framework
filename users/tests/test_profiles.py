import pytest


@pytest.mark.django_db
class TestAdminProfileAccess:
    def test_admin_can_list_profiles(self, admin_client, profile):
        response = admin_client.get("/api/users/profiles/")
        assert response.status_code == 200
        assert response.data["count"] >= 1
        assert any(
            p["phone_number"] == profile.phone_number for p in response.data["results"]
        )

    def test_admin_can_patch_profile(self, admin_client, profile):
        url = f"/api/users/profiles/{profile.id}/"
        response = admin_client.patch(url, {"phone_number": "0987654321"})
        assert response.status_code == 200
        assert response.data["phone_number"] == "0987654321"

    def test_admin_can_create_profile_for_user(self, admin_client, user):
        payload = {
            "user": user.id,
            "phone_number": "0611223344",
            "date_of_birth": "1990-01-01",
        }
        response = admin_client.post("/api/users/profiles/", payload)
        assert response.status_code == 201
        assert response.data["user"] == user.id


@pytest.mark.django_db
class TestUserCannotAccessOthersProfiles:
    def test_user_cannot_list_profiles(self, auth_client):
        response = auth_client.get("/api/users/profiles/")
        assert response.status_code == 403

    def test_user_cannot_access_other_profile(self, auth_client, profile):
        url = f"/api/users/profiles/{profile.id}/"
        response = auth_client.get(url)
        assert response.status_code == 403
