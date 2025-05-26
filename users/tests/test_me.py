import pytest


@pytest.mark.django_db
class TestAddressViaMe:
    def test_list_me_addresses(self, auth_client, address):
        response = auth_client.get("/api/me/addresses/")
        assert response.status_code == 200
        results = response.data["results"]
        assert isinstance(results, list)
        assert any(addr["city"] == "Amsterdam" for addr in results)

    def test_create_me_address(self, auth_client):
        payload = {
            "label": "Work",
            "street": "Office Street",
            "number": "10",
            "zipcode": "5678CD",
            "city": "Utrecht",
            "country": "Netherlands",
            "is_billing": False,
            "is_shipping": True,
        }
        response = auth_client.post("/api/me/addresses/", payload)
        assert response.status_code == 201
        assert response.data["label"] == "Work"
        assert response.data["city"] == "Utrecht"

    def test_create_invalid_address(self, auth_client):
        payload = {
            "label": "Incomplete",
            "zipcode": "1234AB",
            "city": "Leiden",
            "country": "Netherlands",
        }
        response = auth_client.post("/api/me/addresses/", payload)
        assert response.status_code == 400
        assert "street" in response.data
        assert "number" in response.data


@pytest.mark.django_db
class TestMeDelete:
    def test_user_can_soft_delete_own_account(self, auth_client, user):
        # Before: user is active
        assert user.is_active is True

        response = auth_client.delete("/api/me/delete/")
        assert response.status_code == 204

        # After: user still exists, but is inactive
        user.refresh_from_db()
        assert user.is_active is False

    def test_unauthenticated_cannot_delete(self, api_client):
        response = api_client.delete("/api/me/delete/")
        assert response.status_code == 401
