import pytest

from users.models import Address, CustomerProfile


@pytest.mark.django_db
class TestMeAddressFilters:
    @pytest.fixture(autouse=True)
    def init_addresses(self, auth_client, user):
        """
        Clear existing addresses and create three distinct addresses for testing filters, search, and ordering.
        """
        # Remove any pre-existing addresses for this user
        CustomerProfile.objects.filter(user=user).delete()
        Address.objects.filter(profile__user=user).delete()

        # Create profile and new addresses
        profile, _ = CustomerProfile.objects.get_or_create(user=user)
        Address.objects.bulk_create(
            [
                Address(
                    profile=profile,
                    label="Home",
                    street="Langestraat",
                    number="1",
                    zipcode="1111AA",
                    city="Utrecht",
                    country="NL",
                ),
                Address(
                    profile=profile,
                    label="Work",
                    street="Kortestraat",
                    number="2",
                    zipcode="2222BB",
                    city="Amsterdam",
                    country="NL",
                ),
                Address(
                    profile=profile,
                    label="Holiday",
                    street="Zeedijk",
                    number="3",
                    zipcode="3333CC",
                    city="Den Haag",
                    country="NL",
                ),
            ]
        )
        self.url = "/api/users/me/addresses/"

    def test_filter_by_city(self, auth_client):
        response = auth_client.get(f"{self.url}?city=Utrecht")
        assert response.status_code == 200
        payload = response.json()
        results = payload.get("results", payload)
        assert len(results) == 1
        assert results[0]["city"] == "Utrecht"

    def test_filter_boolean_is_billing(self, auth_client, user):
        # Mark the first address as billing
        profile = CustomerProfile.objects.get(user=user)
        addresses = Address.objects.filter(profile=profile)
        addresses[0].is_billing = True
        addresses[0].save()

        response = auth_client.get(f"{self.url}?is_billing=True")
        assert response.status_code == 200
        payload = response.json()
        results = payload.get("results", payload)
        # All returned items should have is_billing == True
        assert all(item["is_billing"] for item in results)

    def test_search_street_partial(self, auth_client):
        response = auth_client.get(f"{self.url}?search=straat")
        assert response.status_code == 200
        payload = response.json()
        results = payload.get("results", payload)
        labels = {item["label"] for item in results}
        assert labels == {"Home", "Work"}

    def test_ordering_zipcode_asc(self, auth_client):
        response = auth_client.get(f"{self.url}?ordering=zipcode")
        assert response.status_code == 200
        payload = response.json()
        results = payload.get("results", payload)
        zipcodes = [item["zipcode"] for item in results]
        assert zipcodes == sorted(zipcodes)

    def test_ordering_zipcode_desc(self, auth_client):
        response = auth_client.get(f"{self.url}?ordering=-zipcode")
        assert response.status_code == 200
        payload = response.json()
        results = payload.get("results", payload)
        zipcodes = [item["zipcode"] for item in results]
        assert zipcodes == sorted(zipcodes, reverse=True)
