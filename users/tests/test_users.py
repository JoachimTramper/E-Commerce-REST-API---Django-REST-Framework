import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestAdminUserViewSet:
    endpoint = "/api/users/users/"

    def test_admin_can_list_users(self, admin_client, user):
        response = admin_client.get(self.endpoint)
        assert response.status_code == 200
        payload = response.json()
        assert payload["count"] >= 1
        assert any(u["email"] == user.email for u in payload["results"])

    def test_non_admin_cannot_access_user_list(self, auth_client):
        response = auth_client.get(self.endpoint)
        assert response.status_code == 403

    def test_admin_can_retrieve_user(self, admin_client, user):
        url = f"{self.endpoint}{user.id}/"
        response = admin_client.get(url)
        assert response.status_code == 200
        assert response.json()["id"] == user.id

    def test_non_admin_cannot_retrieve_user(self, auth_client, user):
        url = f"{self.endpoint}{user.id}/"
        response = auth_client.get(url)
        assert response.status_code == 403

    def test_admin_can_create_user(self, admin_client):
        payload = {
            "email": "new@example.com",
            "username": "newuser",
            "password": "StrongPass123",
        }
        response = admin_client.post(self.endpoint, payload)
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "new@example.com"
        assert "password" not in data

    def test_non_admin_cannot_create_user(self, auth_client):
        payload = {
            "email": "x@x.com",
            "username": "xuser",
            "password": "testpass",
        }
        response = auth_client.post(self.endpoint, payload)
        assert response.status_code == 403

    def test_admin_can_patch_user(self, admin_client, user):
        url = f"{self.endpoint}{user.id}/"
        response = admin_client.patch(url, {"username": "updateduser"})
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "updateduser"
        user.refresh_from_db()
        assert user.username == "updateduser"

    def test_admin_can_delete_user(self, admin_client, user):
        url = f"{self.endpoint}{user.id}/"
        response = admin_client.delete(url)
        assert response.status_code == 204
        # after soft delete, user should still exist but be inactive
        response = admin_client.get(url)
        assert response.status_code == 404
