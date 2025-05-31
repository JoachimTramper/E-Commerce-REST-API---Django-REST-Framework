from datetime import datetime

import django.views.decorators.cache as _cache_mod
import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.utils import timezone
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework.throttling import (
    AnonRateThrottle,
    ScopedRateThrottle,
    SimpleRateThrottle,
    UserRateThrottle,
)
from rest_framework_simplejwt.tokens import RefreshToken

from shop.models import Order, OrderItem, Product
from shop.views import ProductViewSet

User = get_user_model()


#
# ─── GLOBAL CLIENT FIXTURES ─────────────────────────────────────────────────────
#
@pytest.fixture(scope="function")
def api_client():
    # alias for users/tests
    return APIClient()


#
# ─── USER FIXTURE ────────────────────────────────────────────────────────────────
#
@pytest.fixture(scope="function")
def user(db):
    return User.objects.create_user(
        username="testuser", email="foo@bar.com", password="UncommonP4ssw0rd!"
    )


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(
        username="admin",
        email="admin@bar.com",
        password="password123",
        is_staff=True,
        is_superuser=True,
    )


#
# ─── AUTHENTICATED CLIENTS ───────────────────────────────────────────────────────
#
@pytest.fixture(scope="function")
def auth_client(api_client, user):
    token = RefreshToken.for_user(user).access_token
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


@pytest.fixture(scope="function")
def admin_client(api_client, admin_user):
    token = RefreshToken.for_user(admin_user).access_token
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api_client


#
# ─── SHOP-SPECIFIC FIXTURES ──────────────────────────────────────────────────────
#
@pytest.fixture(scope="function")
def shop_user(user):
    """
    Upgrade the normal user so they can add products.
    Use this in shop tests if you need the add_product perm.
    """
    perm = Permission.objects.get(codename="add_product")
    user.user_permissions.add(perm)
    return user


@pytest.fixture(scope="function")
def no_order_user(user):
    """
    A user who has never placed an order.
    Reuses the `user` fixture.
    """
    return user


@pytest.fixture(scope="function")
def products(db):
    return Product.objects.bulk_create(
        [
            Product(name="Cheap", price=1.0, stock=10, description=""),
            Product(name="Mid", price=5.0, stock=0, description=""),
            Product(name="Exp", price=10.0, stock=5, description=""),
        ]
    )


@pytest.fixture(scope="function")
def orders(db, django_user_model):
    u1 = django_user_model.objects.create_user("alice", "a@e.com", "pass")
    u2 = django_user_model.objects.create_user("bob", "b@e.com", "pass")
    p = Product.objects.create(name="P", price=10, stock=5)

    o1 = Order.objects.create(user=u1, status=Order.StatusChoices.PENDING)
    OrderItem.objects.create(order=o1, product=p, quantity=2, price=10)

    o2 = Order.objects.create(user=u2, status=Order.StatusChoices.CONFIRMED)
    OrderItem.objects.create(order=o2, product=p, quantity=1, price=10)

    o3 = Order.objects.create(user=u1, status=Order.StatusChoices.CONFIRMED)
    OrderItem.objects.create(order=o3, product=p, quantity=1, price=5)

    return dict(u1=u1, u2=u2, o1=o1, o2=o2, o3=o3)


@pytest.fixture(scope="function")
def items(db, django_user_model):
    user = django_user_model.objects.create_user("charlie", "c@e.com", "pass")
    p1 = Product.objects.create(name="P1", price=5, stock=5, description="")
    p2 = Product.objects.create(name="P2", price=15, stock=5, description="")

    o1 = Order.objects.create(user=user, status=Order.StatusChoices.PENDING)
    o2 = Order.objects.create(user=user, status=Order.StatusChoices.CONFIRMED)
    i1 = OrderItem.objects.create(order=o1, product=p1, quantity=1, price=5)
    i2 = OrderItem.objects.create(order=o1, product=p2, quantity=3, price=15)
    i3 = OrderItem.objects.create(order=o2, product=p1, quantity=2, price=5)

    return dict(user=user, i1=i1, i2=i2, i3=i3, o1=o1, o2=o2, p1=p1, p2=p2)


@pytest.fixture(scope="function")
def item_client(api_client, items):
    api_client.force_authenticate(user=items["user"])
    return api_client


@pytest.fixture
def cart_with_one_item(db, products, no_order_user):
    order = Order.objects.create(user=no_order_user, status=Order.StatusChoices.PENDING)
    OrderItem.objects.create(
        order=order, product=products[0], quantity=1, price=products[0].price
    )
    return order


@pytest.fixture
def cart_with_items(db, products, no_order_user):
    order = Order.objects.create(user=no_order_user, status=Order.StatusChoices.PENDING)
    OrderItem.objects.create(
        order=order, product=products[0], quantity=2, price=products[0].price
    )
    OrderItem.objects.create(
        order=order, product=products[1], quantity=3, price=products[1].price
    )
    return order


#
# ─── DISABLE THROTTLING EVERYWHERE EXCEPT test_throttling.py ────────────────────
#


@pytest.fixture(autouse=True)
def disable_all_throttling(monkeypatch, request):
    """
    Disable DRF throttling in every test except test_throttling.py.
    """
    if request.fspath.basename not in (
        "test_throttling_shop.py",
        "test_throttling_users.py",
    ):
        for cls in (
            SimpleRateThrottle,
            AnonRateThrottle,
            UserRateThrottle,
            ScopedRateThrottle,
        ):
            monkeypatch.setattr(cls, "allow_request", lambda self, request, view: True)


#
# ─── DISABLE CACHING EVERYWHERE EXEPT test_caching.py──────────────────────────────
#


@pytest.fixture(autouse=True)
def disable_all_caching(monkeypatch, request):
    """
    Disable the cache_page decorator in every test except
    test_caching.py and test_throttling.py.
    """
    if request.fspath.basename not in (
        "test_caching.py",
        "test_throttling_shop.py",
        "test_throttling_users.py",
    ):
        monkeypatch.setattr(
            _cache_mod,
            "cache_page",
            lambda timeout, *args, **kwargs: (lambda view_func: view_func),
        )


@pytest.fixture(autouse=True)
def disable_view_level_caching(monkeypatch, request):
    """
    Unwrap any existing @cache_page on ProductViewSet.list and .retrieve
    except in test_caching.py and test_throttling.py.
    """
    if request.fspath.basename not in (
        "test_caching.py",
        "test_throttling_shop.py",
        "test_throttling_users.py",
    ):
        # Unwrap `list`
        if hasattr(ProductViewSet.list, "__wrapped__"):
            monkeypatch.setattr(ProductViewSet, "list", ProductViewSet.list.__wrapped__)
        # Unwrap `retrieve`
        if hasattr(ProductViewSet.retrieve, "__wrapped__"):
            monkeypatch.setattr(
                ProductViewSet, "retrieve", ProductViewSet.retrieve.__wrapped__
            )


#
# ─── PERIODIC TASKS ───────────────────────────────────────────────────────────────
#


@pytest.fixture(autouse=True)
def celery_eager_settings(settings):
    settings.CELERY_TASK_ALWAYS_EAGER = True
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


@pytest.fixture(autouse=True)
def freeze_time(monkeypatch):
    fixed_now = timezone.make_aware(datetime(2025, 5, 23, 12, 0, 0))
    monkeypatch.setattr(timezone, "now", lambda: fixed_now)
    return fixed_now


@pytest.fixture
def user_factory():
    return lambda **kwargs: baker.make("users.User", **kwargs)


@pytest.fixture
def order_factory():
    return lambda **kwargs: baker.make("shop.Order", **kwargs)


@pytest.fixture
def product_factory():
    return lambda **kwargs: baker.make("shop.Product", **kwargs)


@pytest.fixture
def order_item_factory():
    return lambda **kwargs: baker.make("shop.OrderItem", **kwargs)


#
# ─── USERS-SPECIFIC FIXTURES ─────────────────────────────────────────────────────
#


@pytest.fixture
def profile(user):
    from users.models import CustomerProfile

    return CustomerProfile.objects.create(user=user, phone_number="0611223344")


@pytest.fixture
def address(profile):
    from users.models import Address

    return Address.objects.create(
        profile=profile,
        label="Thuis",
        street="Voorbeeldstraat",
        number="1",
        zipcode="1234AB",
        city="Amsterdam",
        country="Nederland",
        is_billing=True,
        is_shipping=True,
    )
