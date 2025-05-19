import pytest
from django.core.cache import caches
from django.urls import reverse


@pytest.mark.django_db
class TestCaching:
    def test_product_detail_cached(self, client, products):
        """
        1) First GET /products/<pk>/ populates the cache.
        2) Modify the product.
        3) Second GET still returns the original (cached) data.
        """
        cache = caches["default"]
        cache.clear()

        product = products[0]
        url = reverse("shop:products-detail", args=[product.pk])

        resp1 = client.get(url)
        assert resp1.status_code == 200
        data1 = resp1.json()

        product.name = "ChangedName"
        product.save()

        resp2 = client.get(url)
        assert resp2.status_code == 200
        data2 = resp2.json()

        assert data1 == data2

    def test_product_detail_cache_header(self, client, products):
        """Ensure the Cache-Control header is set correctly."""
        product = products[0]
        url = reverse("shop:products-detail", args=[product.pk])

        resp = client.get(url)
        assert resp.status_code == 200
        assert resp["Cache-Control"] == "public, max-age=300"
