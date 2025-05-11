import pytest
from django.contrib.auth import get_user_model

from shop.models import Order, OrderItem, Product

User = get_user_model()


class TestProductModel:
    @pytest.fixture(autouse=True)
    def setup_products(self, db):
        self.product_in_stock = Product.objects.create(
            name="TestProduct1", description="A product in stock", price=10.00, stock=5
        )
        self.product_out_of_stock = Product.objects.create(
            name="TestProduct2", description="Out of stock product", price=5.00, stock=0
        )

    def test_str_returns_name(self):
        assert str(self.product_in_stock) == "TestProduct1"
        assert str(self.product_out_of_stock) == "TestProduct2"

    def test_in_stock_property(self):
        assert self.product_in_stock.in_stock is True
        assert self.product_out_of_stock.in_stock is False


class TestOrderModel:
    @pytest.fixture(autouse=True)
    def setup_order(self, db):
        self.user = User.objects.create_user(
            username="user1", email="user1@example.com", password="pass"
        )
        self.p1 = Product.objects.create(name="A", description="", price=2.50, stock=10)
        self.p2 = Product.objects.create(name="B", description="", price=1.75, stock=20)
        # Clear existing orders to reset numbering
        Order.objects.all().delete()

    def test_order_number_auto_increment(self):
        o1 = Order.objects.create(user=self.user)  # status = Pending
        o1.status = Order.StatusChoices.CONFIRMED  # status = Confirmed
        o1.save()
        o2 = Order.objects.create(user=self.user)
        assert o2.order_number == o1.order_number + 1

    def test_str_returns_order_number_and_username(self):
        order = Order.objects.create(user=self.user)
        expected = f"Order {order.order_number} by {self.user.username}"
        assert str(order) == expected

    def test_total_amount_property(self):
        order = Order.objects.create(user=self.user)
        OrderItem.objects.create(order=order, product=self.p1, quantity=2)
        OrderItem.objects.create(order=order, product=self.p2, quantity=3)
        assert order.total_amount == pytest.approx(10.25)


class TestOrderItemModel:
    @pytest.fixture(autouse=True)
    def setup_item(self, db):
        self.user = User.objects.create_user(
            username="user2", email="u2@example.com", password="pass"
        )
        self.product = Product.objects.create(
            name="C", description="", price=4.00, stock=8
        )
        self.order = Order.objects.create(user=self.user)

    def test_item_subtotal_property(self):
        item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=3
        )
        assert item.item_subtotal == pytest.approx(12.00)

    def test_str_includes_quantity_name_and_order_id(self):
        item = OrderItem.objects.create(
            order=self.order, product=self.product, quantity=1
        )
        expected = f"1 x {self.product.name} (Order {self.order.order_id})"
        assert str(item) == expected
