import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from shop.models import Order, OrderItem, Product

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


# Filtering -- Product
@pytest.mark.django_db
class TestProductFiltering:
    @pytest.fixture(autouse=True)
    def setup_products(self):
        # Price range: 1, 5, 10
        from shop.models import Product

        Product.objects.bulk_create(
            [
                Product(name="Cheap", description="", price=1.00, stock=10),
                Product(name="Mid", description="", price=5.00, stock=0),
                Product(name="Exp", description="", price=10.00, stock=5),
            ]
        )
        self.url = "/api/shop/products/"

    def test_filter_price_min(self, api_client):
        resp = api_client.get(self.url + "?price_min=5")
        assert resp.status_code == status.HTTP_200_OK
        prices = {float(p["price"]) for p in resp.data["results"]}
        assert prices == {5.00, 10.00}

    def test_filter_price_max(self, api_client):
        resp = api_client.get(self.url + "?price_max=5")
        assert resp.status_code == status.HTTP_200_OK
        prices = {float(p["price"]) for p in resp.data["results"]}
        assert prices == {1.00, 5.00}

    def test_filter_in_stock(self, api_client):
        resp = api_client.get(self.url + "?in_stock=true")
        assert resp.status_code == status.HTTP_200_OK
        names = {p["name"] for p in resp.data["results"]}
        assert names == {"Cheap", "Exp"}

    def test_filter_name_contains(self, api_client):
        resp = api_client.get(self.url + "?name=ea")
        assert resp.status_code == status.HTTP_200_OK
        names = {p["name"] for p in resp.data["results"]}
        assert names == {"Cheap"}


# Filtering -- Order
@pytest.mark.django_db
class TestOrderFiltering:
    @pytest.fixture(autouse=True)
    def setup_orders(self, api_client, django_user_model):
        # maak twee users aan
        self.user1 = django_user_model.objects.create_user("alice", "a@x.com", "pass")
        self.user2 = django_user_model.objects.create_user("bob", "b@x.com", "pass")

        # maak twee producten voor de totaalsommen
        p1 = Product.objects.create(name="P1", description="", price=10.00, stock=5)
        p2 = Product.objects.create(name="P2", description="", price=20.00, stock=5)

        # Order A: pending, totaal = 2×10 = 20
        o1 = Order.objects.create(user=self.user1, status="pending")
        OrderItem.objects.create(order=o1, product=p1, quantity=2, price=10.00)

        # Order B: paid, totaal = 1×10 + 2×20 = 50
        o2 = Order.objects.create(user=self.user2, status="paid")
        OrderItem.objects.create(order=o2, product=p1, quantity=1, price=10.00)
        OrderItem.objects.create(order=o2, product=p2, quantity=2, price=20.00)

        # Order C: pending, totaal = 1×5 = 5
        o3 = Order.objects.create(user=self.user1, status="pending")
        OrderItem.objects.create(order=o3, product=p1, quantity=1, price=5.00)

        self.url = "/api/shop/orders/"

    def test_filter_by_status(self, api_client):
        # list/retrieve requires auth
        api_client.force_authenticate(user=self.user1)
        resp = api_client.get(f"{self.url}?status=pending")
        assert resp.status_code == status.HTTP_200_OK
        statuses = {o["status"] for o in resp.data["results"]}
        assert statuses == {"pending"}

    def test_filter_total_min(self, api_client):
        api_client.force_authenticate(user=self.user2)
        resp = api_client.get(f"{self.url}?total_min=30")
        assert resp.status_code == status.HTTP_200_OK
        # alleen order B heeft totaal ≥ 30
        totals = [
            sum(item["quantity"] * float(item["price"]) for item in order["items"])
            for order in resp.data["results"]
        ]
        assert totals == [50.0]

    def test_filter_total_max(self, api_client):
        api_client.force_authenticate(user=self.user1)
        resp = api_client.get(f"{self.url}?total_max=20")
        assert resp.status_code == status.HTTP_200_OK
        # order A (20) and C (5)
        totals = {
            sum(item["quantity"] * float(item["price"]) for item in order["items"])
            for order in resp.data["results"]
        }
        assert totals == {5.0, 20.0}

    def test_filter_created_range(self, api_client):
        api_client.force_authenticate(user=self.user1)
        # set date in past
        past_date = (timezone.now() - timezone.timedelta(days=365)).date().isoformat()
        resp = api_client.get(f"{self.url}?created_after={past_date}")
        assert resp.status_code == status.HTTP_200_OK
        # alle orders zijn later dan een jaar geleden
        assert len(resp.data["results"]) == 2


# Filtering -- OrderItem
@pytest.mark.django_db
class TestOrderItemFiltering:
    @pytest.fixture(autouse=True)
    def setup_items(self, api_client, django_user_model):
        self.user = django_user_model.objects.create_user("charlie", "c@x.com", "pass")
        api_client.force_authenticate(user=self.user)

        # twee orders
        o1 = Order.objects.create(user=self.user, status="pending")
        o2 = Order.objects.create(user=self.user, status="paid")

        # twee producten
        p1 = Product.objects.create(name="P1", description="", price=5.00, stock=5)
        p2 = Product.objects.create(name="P2", description="", price=15.00, stock=5)

        # verschillende orderitems
        OrderItem.objects.create(order=o1, product=p1, quantity=1, price=5.00)
        OrderItem.objects.create(order=o1, product=p2, quantity=3, price=15.00)
        OrderItem.objects.create(order=o2, product=p1, quantity=2, price=5.00)

        self.url = "/api/shop/order-items/"

    def test_filter_by_order(self, api_client):
        api_client.force_authenticate(user=self.user)
        first_uuid = str(OrderItem.objects.first().order.order_id)
        resp = api_client.get(f"{self.url}?order={first_uuid}")
        assert resp.status_code == status.HTTP_200_OK
        order_ids = {item["order"] for item in resp.data["results"]}
        assert order_ids == {first_uuid}

    def test_filter_by_product(self, api_client):
        api_client.force_authenticate(user=self.user)
        resp = api_client.get(f"{self.url}?product={Product.objects.first().id}")
        assert resp.status_code == status.HTTP_200_OK
        product_ids = {item["product"] for item in resp.data["results"]}
        # er zijn twee items met product=1 (één in o1 en één in o2)
        assert product_ids == {Product.objects.first().id}

    def test_filter_quantity_min(self, api_client):
        api_client.force_authenticate(user=self.user)
        resp = api_client.get(f"{self.url}?quantity_min=2")
        assert resp.status_code == status.HTTP_200_OK
        quantities = {item["quantity"] for item in resp.data["results"]}
        assert quantities == {2, 3}

    def test_filter_quantity_max(self, api_client):
        api_client.force_authenticate(user=self.user)
        resp = api_client.get(f"{self.url}?quantity_max=2")
        assert resp.status_code == status.HTTP_200_OK
        quantities = {item["quantity"] for item in resp.data["results"]}
        assert quantities == {1, 2}
