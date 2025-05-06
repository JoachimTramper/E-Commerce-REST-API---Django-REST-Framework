import pytest
from rest_framework import status

from shop.models import Product


@pytest.fixture
def products(db):
    return Product.objects.bulk_create(
        [
            Product(name="Cheap", price=1.0, stock=10, description=""),
            Product(name="Mid", price=5.0, stock=0, description=""),
            Product(name="Exp", price=10.0, stock=5, description=""),
        ]
    )


PRODUCT_LIST = "/api/shop/products/"


def PRODUCT_DETAIL(pk):
    return f"{PRODUCT_LIST}{pk}/"


class TestProductRead:
    def test_list_public(self, api_client, products):
        resp = api_client.get(PRODUCT_LIST)
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["count"] == 3

    def test_retrieve_public(self, api_client, products):
        resp = api_client.get(PRODUCT_DETAIL(products[0].pk))
        assert resp.status_code == status.HTTP_200_OK
        assert resp.data["name"] == products[0].name


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


class TestProductPagination:
    @pytest.fixture(autouse=True)
    def many_products(self, db):
        for i in range(15):
            Product.objects.create(name=f"P{i}", price=1, stock=1)

    def test_is_paginated(self, api_client):
        resp = api_client.get(PRODUCT_LIST)
        assert "results" in resp.data and len(resp.data["results"]) <= 10


@pytest.mark.parametrize(
    "param,value,expected",
    [
        ("price_min", 5, {"Mid", "Exp"}),
        ("price_max", 5, {"Cheap", "Mid"}),
        ("in_stock", True, {"Cheap", "Exp"}),
        ("name", "ea", {"Cheap"}),
    ],
)
def test_product_filters(auth_client, products, param, value, expected):
    resp = auth_client.get(f"{PRODUCT_LIST}?{param}={value}")
    assert resp.status_code == status.HTTP_200_OK
    names = {p["name"] for p in resp.data["results"]}
    assert names == expected
