import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestUserAuthorization:
    def test_access_protected_endpoint_without_token(self, api_client):
        url = reverse("users:users-list")
        resp = api_client.get(url)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_access_protected_endpoint_with_invalid_token(self, api_client):
        api_client.credentials(HTTP_AUTHORIZATION="Bearer invalid.token.here")
        url = reverse("users:users-list")
        resp = api_client.get(url)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_non_admin_cannot_delete_other_user(self, auth_client, user, admin_user):
        url = reverse("users:users-detail", args=[admin_user.id])
        resp = auth_client.delete(url)
        assert resp.status_code == status.HTTP_403_FORBIDDEN
