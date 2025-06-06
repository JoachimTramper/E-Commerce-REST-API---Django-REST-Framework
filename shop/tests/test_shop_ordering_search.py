import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestProductOrdering:
    def test_order_products_by_name_ascending(self, auth_client, product_factory):
        product_factory(name="Apple", price=1.00, stock=5, description="")
        product_factory(name="Banana", price=1.00, stock=5, description="")

        url = reverse("shop:products-list") + "?ordering=name"
        resp = auth_client.get(url)

        assert resp.status_code == status.HTTP_200_OK
        results = resp.json()["results"]
        names = [item["name"] for item in results]

        # 'Apple' has to come before 'Banana'
        assert names.index("Apple") < names.index("Banana")

    def test_order_products_by_price_descending(self, auth_client, product_factory):
        product_factory(name="Cheap", price=1.00, stock=5, description="")
        product_factory(name="Expensive", price=9.99, stock=5, description="")

        url = reverse("shop:products-list") + "?ordering=-price"
        resp = auth_client.get(url)

        assert resp.status_code == status.HTTP_200_OK
        results = resp.json()["results"]
        # most expensive product (0.99) should be first
        assert float(results[0]["price"]) >= float(results[1]["price"])


@pytest.mark.django_db
class TestProductSearch:
    def test_search_products_by_description_substring(
        self, auth_client, product_factory
    ):
        target = product_factory(
            name="X", price=2.50, stock=4, description="Unique description"
        )
        product_factory(
            name="Y", price=2.50, stock=4, description="General description"
        )

        url = reverse("shop:products-list") + "?search=Unique"

        resp = auth_client.get(url)
        assert resp.status_code == status.HTTP_200_OK

        results = resp.json().get("results", [])

        assert any(
            item["id"] == target.id for item in results
        ), f"Target ID {target.id} not found in results"
        assert all("Unique" in item["description"] for item in results)
