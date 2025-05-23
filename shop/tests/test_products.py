import pytest
from django.urls import reverse
from rest_framework import status

from shop.models import Product

PRODUCT_LIST = "/api/shop/products/"


def PRODUCT_DETAIL(pk):
    return f"{PRODUCT_LIST}{pk}/"


@pytest.mark.django_db
class TestProductRead:
    def test_list_public(self, api_client, products):
        resp = api_client.get(PRODUCT_LIST)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == 3

    def test_retrieve_public(self, api_client, products):
        resp = api_client.get(PRODUCT_DETAIL(products[0].pk))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["name"] == products[0].name


@pytest.mark.django_db
class TestProductCRUDPermissions:
    def test_create_requires_auth(self, api_client):
        resp = api_client.post(PRODUCT_LIST, {"name": "X", "price": 1, "stock": 1})
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_normal_user_forbidden(self, auth_client):
        resp = auth_client.post(PRODUCT_LIST, {"name": "X", "price": 1, "stock": 1})
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_create(self, admin_client):
        resp = admin_client.post(
            PRODUCT_LIST, {"name": "Y", "price": 2, "stock": 2, "description": "new"}
        )
        assert resp.status_code == status.HTTP_201_CREATED

    def test_normal_update_forbidden(self, auth_client, products):
        resp = auth_client.patch(PRODUCT_DETAIL(products[0].pk), {"price": 9})
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_update(self, admin_client, products):
        resp = admin_client.patch(PRODUCT_DETAIL(products[0].pk), {"price": 9})
        assert resp.status_code == status.HTTP_200_OK

    def test_normal_delete_forbidden(self, auth_client, products):
        resp = auth_client.delete(PRODUCT_DETAIL(products[0].pk))
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_admin_can_delete(self, admin_client, products):
        resp = admin_client.delete(PRODUCT_DETAIL(products[0].pk))
        assert resp.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
class TestProductPagination:
    @pytest.fixture(autouse=True)
    def many_products(self, db):
        for i in range(15):
            Product.objects.create(name=f"P{i}", price=1, stock=1)

    def test_is_paginated(self, api_client):
        resp = api_client.get(PRODUCT_LIST)
        assert "results" in resp.data and len(resp.data["results"]) <= 10


@pytest.mark.django_db
class TestProductFilters:
    @pytest.mark.parametrize(
        "param,value,expected_names",
        [
            ("price_min", 5, {"Mid", "Exp"}),
            ("price_max", 5, {"Cheap", "Mid"}),
            ("in_stock", True, {"Cheap", "Exp"}),
            ("name", "ea", {"Cheap"}),
        ],
    )
    def test_filters_on_list(self, auth_client, products, param, value, expected_names):
        """
        Ensure that the filters price_min, price_max, in_stock and name work.
        """
        url = reverse("shop:products-list") + f"?{param}={value}"
        resp = auth_client.get(url)

        assert resp.status_code == status.HTTP_200_OK
        names = {item["name"] for item in resp.data["results"]}
        assert names == expected_names


@pytest.mark.django_db
class TestProductEdgeCases:
    def test_retrieve_nonexistent_returns_404(self, api_client):
        resp = api_client.get(PRODUCT_DETAIL(9999))
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_patch_nonexistent_returns_404(self, admin_client):
        resp = admin_client.patch(PRODUCT_DETAIL(9999), {"price": 1}, format="json")
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_nonexistent_returns_404(self, admin_client):
        resp = admin_client.delete(PRODUCT_DETAIL(9999))
        assert resp.status_code == status.HTTP_404_NOT_FOUND

    def test_create_invalid_data_returns_400(self, admin_client):
        payload = {"name": "", "price": -1, "stock": -5, "description": ""}
        resp = admin_client.post(PRODUCT_LIST, payload, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        for field in ("name", "price", "stock"):
            assert field in resp.data

    def test_update_invalid_data_returns_400(self, admin_client, products):
        pk = products[0].pk
        payload = {"price": -10, "stock": -1}
        resp = admin_client.patch(PRODUCT_DETAIL(pk), payload, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        assert "price" in resp.data and "stock" in resp.data

    def test_ordering_by_price(self, api_client, products):
        resp_asc = api_client.get(f"{PRODUCT_LIST}?ordering=price")
        prices_asc = [float(p["price"]) for p in resp_asc.data["results"]]
        assert prices_asc == sorted(prices_asc)

        resp_desc = api_client.get(f"{PRODUCT_LIST}?ordering=-price")
        prices_desc = [float(p["price"]) for p in resp_desc.data["results"]]
        assert prices_desc == sorted(prices_desc, reverse=True)

    def test_search_by_name(self, api_client, products):
        unique = products[0]
        unique.name = "UniekXYZ"
        unique.save()

        resp = api_client.get(f"{PRODUCT_LIST}?search=UniekXYZ")
        names = {p["name"] for p in resp.data["results"]}
        assert names == {"UniekXYZ"}
