import pytest


@pytest.mark.django_db
class TestAdminUserViewSet:
    def test_admin_can_list_users(self, admin_client, user):
        response = admin_client.get("/api/users/users/")
        assert response.status_code == 200
        assert any(u["email"] == user.email for u in response.data["results"])

    def test_non_admin_cannot_access_user_list(self, auth_client):
        response = auth_client.get("/api/users/users/")
        assert response.status_code == 403
