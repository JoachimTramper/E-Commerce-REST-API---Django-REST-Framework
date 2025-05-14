import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.throttling import SimpleRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken

from shop.models import Order, OrderItem, Product

User = get_user_model()


@pytest.fixture(scope="function")
def anon_client():
    """
    Always returns a new, unauthenticated API client instance.
    """
    return APIClient()


@pytest.fixture(scope="function")
def auth_client(anon_client, user):
    """
    API client authenticated as a regular user.
    """
    token = RefreshToken.for_user(user).access_token
    anon_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return anon_client


@pytest.fixture(scope="function")
def admin_client(auth_client, user):
    """
    API client authenticated as an admin user.
    """
    user.is_staff = True
    user.save()
    return auth_client


@pytest.fixture(scope="function")
def user(db):
    """
    Creates and returns a non-staff test user.
    """
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="testpass"
    )


@pytest.fixture(scope="function")
def products(db):
    """
    Creates and returns a list of Product instances.
    """
    return Product.objects.bulk_create(
        [
            Product(name="Cheap", price=1.0, stock=10, description=""),
            Product(name="Mid", price=5.0, stock=0, description=""),
            Product(name="Exp", price=10.0, stock=5, description=""),
        ]
    )


@pytest.fixture(scope="function")
def orders(db, django_user_model):
    """
    Creates sample orders and order items without using any API client.
    """
    u1 = django_user_model.objects.create_user("alice", "alice@example.com", "pass")
    u2 = django_user_model.objects.create_user("bob", "bob@example.com", "pass")
    p = Product.objects.create(name="P", price=10, stock=5)

    o1 = Order.objects.create(user=u1, status=Order.StatusChoices.PENDING)
    OrderItem.objects.create(order=o1, product=p, quantity=2, price=10)

    o2 = Order.objects.create(user=u2, status=Order.StatusChoices.CONFIRMED)
    OrderItem.objects.create(order=o2, product=p, quantity=1, price=10)

    o3 = Order.objects.create(user=u1, status=Order.StatusChoices.CONFIRMED)
    OrderItem.objects.create(order=o3, product=p, quantity=1, price=5)

    return {"u1": u1, "u2": u2, "o1": o1, "o2": o2, "o3": o3}


@pytest.fixture(scope="function")
def items(db, django_user_model):
    """
    Creates sample order items for a single user, without API client involvement.
    """
    user = django_user_model.objects.create_user(
        "charlie", "charlie@example.com", "pass"
    )
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


@pytest.fixture(scope="function")
def item_client(anon_client, items):
    """
    API client authenticated as the user who owns the sample items.
    """
    anon_client.force_authenticate(user=items["user"])
    return anon_client


@pytest.fixture
def cart_with_one_item(db, products, no_order_user):
    """
    Creates a user who has exactly one PENDING item in their cart.
    Orders['u1'] is a User instance and products[0] is a Product.
    """
    user = no_order_user
    order = Order.objects.create(user=user, status=Order.StatusChoices.PENDING)
    OrderItem.objects.create(
        order=order,
        product=products[0],
        quantity=1,
        price=products[0].price,
    )
    return order


@pytest.fixture
def cart_with_items(db, products, no_order_user):
    """
    Creates a user with 2 items in thier pending cart.
    """
    user = no_order_user
    order = Order.objects.create(user=user, status=Order.StatusChoices.PENDING)
    # twee items
    OrderItem.objects.create(
        order=order,
        product=products[0],
        quantity=2,
        price=products[0].price,
    )
    OrderItem.objects.create(
        order=order,
        product=products[1],
        quantity=3,
        price=products[1].price,
    )
    return order


@pytest.fixture
def no_order_user(django_user_model):
    """
    Creates a user who has no orders.
    """
    return django_user_model.objects.create_user("carol", "carol@example.com", "pass")


@pytest.fixture(autouse=True)
def disable_all_throttling(monkeypatch):
    """
    Zorgt dat álle DRF-throttle-classes hun allow_request() altijd True teruggeven,
    ongeacht view-instellingen of scope.
    """
    monkeypatch.setattr(
        SimpleRateThrottle, "allow_request", lambda self, request, view: True
    )
