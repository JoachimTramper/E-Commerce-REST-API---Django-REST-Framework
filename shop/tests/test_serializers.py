import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory

from shop.models import Order, Product
from shop.serializers import (
    OrderDetailSerializer,
    OrderItemDetailSerializer,
    ProductSerializer,
)

User = get_user_model()


class TestProductSerializer:
    @pytest.fixture(autouse=True)
    def setup_products(self, db):
        # Create an existing product for update tests
        self.existing = Product.objects.create(
            name="Existing", description="Desc", price=2.00, stock=10
        )

    def test_valid_product_data(self):
        data = {
            "name": "NewProd",
            "description": "New desc",
            "price": "5.50",
            "stock": 3,
        }
        serializer = ProductSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        product = serializer.save()
        assert product.name == "NewProd"
        assert product.stock == 3

    @pytest.mark.parametrize(
        "field, value",
        [
            ("name", None),
            ("description", ""),
            ("price", "-1.00"),
            ("stock", -5),
        ],
    )
    def test_invalid_product_fields(self, field, value):
        payload = {"name": "P", "description": "D", "price": "1.00", "stock": 1}
        payload[field] = value
        serializer = ProductSerializer(data=payload)
        assert not serializer.is_valid()
        assert field in serializer.errors


class TestOrderItemSerializer:
    @pytest.fixture(autouse=True)
    def setup(self, db):
        self.product = Product.objects.create(
            name="ItemProd", description="Desc", price=3.00, stock=5
        )
        self.order = Order.objects.create(
            user=User.objects.create_user("u", "u@test.com", "pw")
        )

    def test_valid_orderitem(self):
        data = {"product_id": self.product.pk, "quantity": 2}
        serializer = OrderItemDetailSerializer(data=data)
        assert serializer.is_valid(), serializer.errors
        item = serializer.save(order=self.order)
        assert item.item_subtotal == self.product.price * 2

    @pytest.mark.parametrize("qty", [0, -1, 10])
    def test_invalid_quantities(self, qty):
        data = {"product_id": self.product.pk, "quantity": qty}
        serializer = OrderItemDetailSerializer(data=data)
        assert not serializer.is_valid()
        assert "quantity" in serializer.errors


# Note: OrderSerializer tests depend on implementation of nested create;
# here we simply validate that items field is required and nested validation works.
class TestOrderSerializer:
    @pytest.fixture(autouse=True)
    def setup(self, db):
        self.user = User.objects.create_user("u2", "u2@test.com", "pw")
        self.product = Product.objects.create(
            name="OP", description="Desc", price=4.00, stock=4
        )
        self.factory = APIRequestFactory()

    def test_order_requires_items(self):
        data = {}
        request = self.factory.post("/fake/")
        request.user = self.user

        serializer = OrderDetailSerializer(data=data, context={"request": request})
        assert not serializer.is_valid()
        assert "items" in serializer.errors

    def test_order_with_items_valid(self):
        data = {"items": [{"product_id": self.product.pk, "quantity": 1}]}
        request = self.factory.post("/fake/")
        request.user = self.user

        serializer = OrderDetailSerializer(data=data, context={"request": request})
        assert serializer.is_valid(), serializer.errors
        order = serializer.save()
        assert order.total_amount == pytest.approx(self.product.price)
        assert order.user == self.user
