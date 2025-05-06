import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from shop.models import Order, OrderItem, Product

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user("testuser", "test@example.com", "testpass")


@pytest.fixture
def auth_client(api_client, user):
    token = RefreshToken.for_user(user).access_token
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.fixture
def admin_client(auth_client, user):
    user.is_staff = True
    user.save()
    return auth_client


@pytest.fixture
def orders(db, auth_client, django_user_model):
    u1 = django_user_model.objects.create_user("alice", "a@", "p")
    u2 = django_user_model.objects.create_user("bob", "b@", "p")
    p = Product.objects.create(name="P", price=10, stock=5)

    o1 = Order.objects.create(user=u1, status=Order.StatusChoices.PENDING)
    OrderItem.objects.create(order=o1, product=p, quantity=2, price=10)

    o2 = Order.objects.create(user=u2, status=Order.StatusChoices.CONFIRMED)
    OrderItem.objects.create(order=o2, product=p, quantity=1, price=10)

    o3 = Order.objects.create(user=u1, status=Order.StatusChoices.PENDING)
    OrderItem.objects.create(order=o3, product=p, quantity=1, price=5)

    return {"u1": u1, "u2": u2, "o1": o1, "o2": o2, "o3": o3}


@pytest.fixture
def items(db, api_client, django_user_model):
    user = django_user_model.objects.create_user("charlie", "c@x.com", "pass")

    p1 = Product.objects.create(name="P1", description="", price=5.00, stock=5)
    p2 = Product.objects.create(name="P2", description="", price=15.00, stock=5)

    o1 = Order.objects.create(user=user, status=Order.StatusChoices.PENDING)
    o2 = Order.objects.create(user=user, status=Order.StatusChoices.CONFIRMED)

    i1 = OrderItem.objects.create(order=o1, product=p1, quantity=1, price=5.00)
    i2 = OrderItem.objects.create(order=o1, product=p2, quantity=3, price=15.00)
    i3 = OrderItem.objects.create(order=o2, product=p1, quantity=2, price=5.00)

    return {
        "user": user,
        "i1": i1,
        "i2": i2,
        "i3": i3,
        "o1": o1,
        "o2": o2,
        "p1": p1,
        "p2": p2,
    }


@pytest.fixture
def item_client(api_client, items):
    """
    - Client for testing order items.
    - Authenticated as the user who created the items.
    """
    api_client.force_authenticate(items["user"])
    return api_client
