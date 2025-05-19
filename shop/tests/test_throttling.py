import pytest
from django.core.cache import caches, close_caches
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework.throttling import ScopedRateThrottle

from shop.views import ProductViewSet


@pytest.fixture(autouse=True)
def reset_cache_and_scope():
    """Clear cache and use only ScopedRateThrottle."""
    close_caches()
    caches["default"].clear()
    ProductViewSet.throttle_classes = [ScopedRateThrottle]


@pytest.mark.django_db
class TestThrottlingSimple:
    def test_anon_get_rate_limit(self):
        """Allow 3 anonymous GETs, throttle on the 4th."""
        ProductViewSet.throttle_scope = "anon"
        client = APIClient()
        url = reverse("shop:products-list")

        for _ in range(3):
            assert client.get(url).status_code == 200

        assert client.get(url).status_code == 429

    def test_user_post_rate_limit(self, admin_client):
        """Allow 3 authenticated POSTs, throttle on the 4th."""
        ProductViewSet.throttle_scope = "write-burst"
        client = admin_client
        url = reverse("shop:products-list")

        for _ in range(3):
            resp = client.post(
                url,
                {"name": "X", "price": 1, "stock": 1, "description": "x"},
                format="json",
            )
            assert resp.status_code in (200, 201)

        assert (
            client.post(
                url,
                {"name": "X4", "price": 1, "stock": 1, "description": "x"},
                format="json",
            ).status_code
            == 429
        )
