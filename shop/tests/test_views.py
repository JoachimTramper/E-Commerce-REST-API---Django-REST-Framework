import pytest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from shop.models import Product

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass123"
    )


@pytest.fixture
def tokens(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)


@pytest.fixture
def auth_client(api_client, tokens):
    access_token, _ = tokens
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client


@pytest.fixture
def admin_client(api_client, user, tokens):
    user.is_staff = True
    user.save()
    access_token, _ = tokens
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
    return api_client


@pytest.fixture
def products(db):
    p1 = Product.objects.create(name="Apple", price=0.50, stock=10)
    p2 = Product.objects.create(name="Pear", price=0.75, stock=20)
    return p1, p2


@pytest.fixture
def urls(products):
    list_url = "/api/shop/products/"
    detail_url = f"{list_url}{products[0].pk}/"
    return list_url, detail_url


# READ Endpoints
class TestProductRead:
    def test_list_products_public(self, api_client, products, urls):
        list_url, _ = urls
        resp = api_client.get(list_url)
        assert resp.status_code == status.HTTP_200_OK

        data = resp.data
        # pagination check
        assert "count" in data
        assert "results" in data

        assert len(data["results"]) == 2

    def test_retrieve_product_public(self, api_client, urls):
        _, detail_url = urls
        resp = api_client.get(detail_url)
        assert resp.status_code == status.HTTP_200_OK
        assert "name" in resp.data


# CREATE Endpoints
class TestProductCreate:
    def test_create_requires_authentication(self, api_client, urls):
        list_url, _ = urls
        data = {"name": "Banaan", "price": 1.00}
        resp = api_client.post(list_url, data, format="json")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_product_not_allowed_for_normal_user(self, auth_client, urls):
        list_url, _ = urls
        data = {"name": "Banaan", "price": 1.00, "stock": 5}
        resp = auth_client.post(list_url, data, format="json")
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_create_product_allowed_for_admin(self, admin_client, urls):
        list_url, _ = urls
        data = {
            "name": "Banaan",
            "price": 1.00,
            "stock": 5,
            "description": "Very tasty banana",
        }
        resp = admin_client.post(list_url, data, format="json")
        assert resp.status_code == status.HTTP_201_CREATED
        assert Product.objects.count() == 3

    def test_invalid_product_data(self, admin_client, urls):
        list_url, _ = urls
        invalid = {"name": "", "price": -1, "stock": None, "description": ""}
        resp = admin_client.post(list_url, invalid, format="json")
        assert resp.status_code == status.HTTP_400_BAD_REQUEST
        for field in ["name", "price", "stock", "description"]:
            assert field in resp.data


# UPDATE Endpoints
class TestProductUpdate:
    def test_update_requires_authentication(self, api_client, urls):
        _, detail_url = urls
        resp = api_client.patch(detail_url, {"price": 0.99}, format="json")
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_forbidden_for_normal_user(self, auth_client, urls):
        _, detail_url = urls
        resp = auth_client.patch(detail_url, {"price": 0.99}, format="json")
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_update_allowed_for_admin(self, admin_client, urls, products):
        _, detail_url = urls
        resp = admin_client.patch(detail_url, {"price": 0.99}, format="json")
        assert resp.status_code == status.HTTP_200_OK
        product = Product.objects.get(pk=products[0].pk)
        assert float(product.price) == 0.99


# DELETE Endpoints
class TestProductDelete:
    def test_delete_requires_authentication(self, api_client, urls):
        _, detail_url = urls
        resp = api_client.delete(detail_url)
        assert resp.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_forbidden_for_normal_user(self, auth_client, urls):
        _, detail_url = urls
        resp = auth_client.delete(detail_url)
        assert resp.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_allowed_for_admin(self, admin_client, urls):
        _, detail_url = urls
        resp = admin_client.delete(detail_url)
        assert resp.status_code == status.HTTP_204_NO_CONTENT
        assert Product.objects.count() == 1


# Pagination
class TestProductPagination:
    @pytest.fixture(autouse=True)
    def setup_products(self, db):
        # Maak 15 producten aan
        for i in range(15):
            Product.objects.create(name=f"P{i}", price=1.00, stock=1)
        self.url = "/api/shop/products/"

    def test_list_is_paginated(self, api_client):
        resp = api_client.get(self.url)
        assert resp.status_code == status.HTTP_200_OK

        data = resp.data
        assert "count" in data
        assert "results" in data
        assert isinstance(data["results"], list)
