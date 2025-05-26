import pytest


@pytest.mark.django_db
class TestAddressDetail:
    def test_patch_address(self, auth_client, address):
        url = f"/api/users/addresses/{address.id}/"
        response = auth_client.patch(url, {"city": "Rotterdam"})
        assert response.status_code == 200
        assert response.data["city"] == "Rotterdam"

    def test_delete_address(self, auth_client, address):
        url = f"/api/users/addresses/{address.id}/"
        response = auth_client.delete(url)
        assert response.status_code == 204

        # Ensure the address is actually deleted
        response = auth_client.get(url)
        assert response.status_code == 404

    def test_other_user_address_is_inaccessible(self, api_client, user):
        from users.models import Address, CustomerProfile, User

        # Create another user with their own address
        other_user = User.objects.create_user(
            email="other@example.com", username="other", password="pass123"
        )
        profile = CustomerProfile.objects.create(user=other_user)
        other_address = Address.objects.create(
            profile=profile,
            label="Private",
            street="Secret",
            number="1",
            zipcode="0000AA",
            city="Hidden",
            country="Nowhere",
        )

        url = f"/api/users/addresses/{other_address.id}/"

        # When unauthenticated → expect 401 Unauthorized
        response = api_client.get(url)
        assert response.status_code == 401

        # When authenticated as test user → expect 404 Not Found (not yours)
        api_client.force_authenticate(user=user)
        response = api_client.get(url)
        assert response.status_code == 404
