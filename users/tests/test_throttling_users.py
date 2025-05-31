import pytest
from django.conf import settings
from django.core.cache import caches, close_caches

from users.views.me import MeAddressListCreateView, MeProfileView


@pytest.fixture(autouse=True)
def reset_cache_and_scope(monkeypatch):
    """Clear cache, override throttle classes and rates for deterministic testing."""
    close_caches()
    caches["default"].clear()

    # Only use ScopedRateThrottle on these views
    from rest_framework.throttling import ScopedRateThrottle

    MeProfileView.throttle_classes = [ScopedRateThrottle]
    MeAddressListCreateView.throttle_classes = [ScopedRateThrottle]

    # Shrink the rates so 4th request triggers 429
    rates = settings.REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]
    rates["read-burst"] = "3/minute"
    rates["write-burst"] = "3/minute"


@pytest.mark.django_db
class TestUsersThrottlingSimple:
    def test_read_burst_me_profile_limit(self, auth_client, profile):
        """Allow 3 GETs to /me/profile/, throttle the 4th."""
        MeProfileView.throttle_scope = "read-burst"
        url = "/api/users/me/profile/"

        for _ in range(3):
            response = auth_client.get(url)
            assert response.status_code == 200

        # 4th request should be throttled
        response = auth_client.get(url)
        assert response.status_code == 429

    def test_write_burst_me_addresses_limit(self, auth_client, user):
        """Allow 3 POSTs to /me/addresses/, throttle the 4th."""
        MeAddressListCreateView.throttle_scope = "write-burst"
        url = "/api/users/me/addresses/"
        payload = {
            "label": "Temp",
            "street": "Test",
            "number": "1",
            "zipcode": "0000AA",
            "city": "City",
            "country": "NL",
        }

        for _ in range(3):
            response = auth_client.post(url, payload, format="json")
            assert response.status_code in (200, 201)

        # 4th request should be throttled
        response = auth_client.post(url, payload, format="json")
        assert response.status_code == 429
