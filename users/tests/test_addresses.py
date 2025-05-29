import pytest

from users.models import Address, CustomerProfile, User


@pytest.mark.django_db
class TestAddressDetail:
    def test_patch_own_address(self, auth_client, address):
        url = f"/api/users/me/addresses/{address.id}/"
        response = auth_client.patch(url, {"city": "Rotterdam"})
        assert response.status_code == 200
        assert response.data["city"] == "Rotterdam"

    def test_delete_own_address(self, auth_client, address):
        url = f"/api/users/me/addresses/{address.id}/"
        response = auth_client.delete(url)
        assert response.status_code == 204

        # it should no longer exist
        response = auth_client.get(url)
        assert response.status_code == 404

    def test_other_user_address_inaccessible(self, api_client, auth_client, address):
        # Create another user and their address
        other_user = User.objects.create_user(
            email="other@example.com", username="other", password="test1234"
        )
        other_profile = CustomerProfile.objects.create(user=other_user)
        other_address = Address.objects.create(
            profile=other_profile,
            label="Private",
            street="Secret St",
            number="1",
            zipcode="0000AA",
            city="Hidden",
            country="Nowhere",
        )

        # unauthenticated → 404 (drf by default)
        url = f"/api/users/me/addresses/{other_address.id}/"
        response = api_client.get(url)
        assert response.status_code == 404

        # authenticated as *fixture-user* → 404 voor een adres dat niet van hem is
        response = auth_client.get(url)
        assert response.status_code == 404


@pytest.mark.django_db
class TestAddressListCreate:
    endpoint = "/api/users/me/addresses/"

    def test_list_requires_auth(self, api_client):
        response = api_client.get(self.endpoint)
        assert response.status_code == 401

    def test_list_returns_only_own(self, auth_client, address):
        response = auth_client.get(self.endpoint)
        assert response.status_code == 200
        payload = response.json()
        data = payload["results"]
        ids = {item["id"] for item in data}
        assert ids == {address.id}

    def test_list_empty_if_no_addresses(self, auth_client, user):
        response = auth_client.get(self.endpoint)
        assert response.status_code == 200
        payload = response.json()
        assert payload["results"] == []
        assert payload["count"] == 0

    def test_create_requires_auth(self, api_client):
        response = api_client.post(self.endpoint, {"city": "Test"})
        assert response.status_code == 401

    def test_create_address(self, auth_client, user):
        payload = {
            "label": "Work",
            "street": "Nieuwe Straat",
            "number": "42",
            "zipcode": "1234AB",
            "city": "Utrecht",
            "country": "NL",
        }
        response = auth_client.post(self.endpoint, payload)
        assert response.status_code == 201

        created = response.json()
        # verify saved fields
        for field, val in payload.items():
            assert created[field] == val
        # linked to correct profile
        address = Address.objects.get(id=created["id"])
        assert address.profile.user == user


@pytest.mark.django_db
class TestAdminAddressList:
    endpoint = "/api/users/addresses/"

    def test_admin_can_list_all(self, admin_client, address):
        # create another address for a different user
        other_user = User.objects.create_user(
            email="admin2@example.com", username="admin2", password="adminpass"
        )
        other_profile = CustomerProfile.objects.create(user=other_user)
        other_address = Address.objects.create(
            profile=other_profile,
            label="Other",
            street="Main St",
            number="10",
            zipcode="1111BB",
            city="City",
            country="Country",
        )

        response = admin_client.get(self.endpoint)
        assert response.status_code == 200
        payload = response.json()
        data = payload["results"]
        ids = {item["id"] for item in data}
        assert address.id in ids and other_address.id in ids

    def test_non_admin_cannot_list_all(self, auth_client):
        response = auth_client.get(self.endpoint)
        assert response.status_code in (403, 404)


@pytest.mark.django_db
class TestAdminAddressCRUD:
    endpoint = "/api/users/addresses/"

    def test_admin_can_create_address(self, admin_client, user):
        profile = CustomerProfile.objects.create(user=user)
        payload = {
            "profile": profile.id,
            "label": "Office",
            "street": "Werkstraat",
            "number": "5",
            "zipcode": "9999ZZ",
            "city": "Den Haag",
            "country": "NL",
            "is_billing": False,
            "is_shipping": True,
        }
        response = admin_client.post(self.endpoint, payload)
        assert response.status_code == 201
        data = response.json()
        assert data["label"] == "Office"
        assert data["profile"] == profile.id

    def test_admin_can_patch_address(self, admin_client, address):
        url = f"{self.endpoint}{address.id}/"
        response = admin_client.patch(url, {"city": "Rotterdam"})
        assert response.status_code == 200
        assert response.json()["city"] == "Rotterdam"
        address.refresh_from_db()
        assert address.city == "Rotterdam"

    def test_admin_can_delete_address(self, admin_client, address):
        url = f"{self.endpoint}{address.id}/"
        response = admin_client.delete(url)
        assert response.status_code == 204
        # after deletion, it should no longer exist
        response = admin_client.get(url)
        assert response.status_code == 404

    def test_non_admin_cannot_create_address(self, auth_client, profile):
        payload = {
            "profile": profile.id,
            "label": "X",
            "street": "Y",
            "number": "1",
            "zipcode": "2",
            "city": "Z",
            "country": "NL",
        }
        response = auth_client.post(self.endpoint, payload)
        assert response.status_code in (403, 404)

    def test_non_admin_cannot_patch_address(self, auth_client, address):
        url = f"{self.endpoint}{address.id}/"
        response = auth_client.patch(url, {"city": "X"})
        assert response.status_code in (403, 404)
