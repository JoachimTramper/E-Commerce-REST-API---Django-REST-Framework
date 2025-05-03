from django.test import TestCase
from django.contrib.auth import get_user_model


from shop.models import Product, Order, OrderItem

User = get_user_model()

class ProductModelTests(TestCase):
    def setUp(self):
        self.product_in_stock = Product.objects.create(
            name="TestProduct1",
            description="A product in stock",
            price=10.00,
            stock=5
        )
        self.product_out_of_stock = Product.objects.create(
            name="TestProduct2",
            description="Out of stock product",
            price=5.00,
            stock=0
        )

    def test_str_returns_name(self):
        self.assertEqual(str(self.product_in_stock), "TestProduct1")
        self.assertEqual(str(self.product_out_of_stock), "TestProduct2")

    def test_in_stock_property(self):
        self.assertTrue(self.product_in_stock.in_stock)
        self.assertFalse(self.product_out_of_stock.in_stock)

class OrderModelTests(TestCase):
    def setUp(self):
        # test user
        self.user = User.objects.create_user(username="user1", email="user1@example.com", password="pass")
        # test products
        self.p1 = Product.objects.create(name="A", description="", price=2.50, stock=10)
        self.p2 = Product.objects.create(name="B", description="", price=1.75, stock=20)
        # clear any existing orders
        Order.objects.all().delete()

    def test_order_number_auto_increment(self):
        o1 = Order.objects.create(user=self.user)
        o2 = Order.objects.create(user=self.user)
        self.assertEqual(o1.order_number + 1, o2.order_number)

    def test_str_returns_order_number_and_username(self):
        order = Order.objects.create(user=self.user)
        expected = f"Order {order.order_number} by {self.user.username}"
        self.assertEqual(str(order), expected)

    def test_total_amount_property(self):
        order = Order.objects.create(user=self.user)
        OrderItem.objects.create(order=order, product=self.p1, quantity=2)
        OrderItem.objects.create(order=order, product=self.p2, quantity=3)
        # subtotal = 2*2.50 + 3*1.75 = 5.00 + 5.25 = 10.25
        self.assertAlmostEqual(order.total_amount, 10.25)

class OrderItemModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="user2", email="u2@example.com", password="pass")
        self.product = Product.objects.create(name="C", description="", price=4.00, stock=8)
        self.order = Order.objects.create(user=self.user)

    def test_item_subtotal_property(self):
        item = OrderItem.objects.create(order=self.order, product=self.product, quantity=3)
        self.assertAlmostEqual(item.item_subtotal, 12.00)

    def test_str_includes_quantity_name_and_order_id(self):
        item = OrderItem.objects.create(order=self.order, product=self.product, quantity=1)
        expected = f"1 x C (Order {self.order.order_id})"
        self.assertEqual(str(item), expected)




# Views

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from shop.models import Product

User = get_user_model()

class ProductAPITests(APITestCase):
    def setUp(self):
        # Create a test user and generate tokens
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpass123")
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.refresh_token = str(refresh)

        # Create sample products
        Product.objects.create(name="Apple", price=0.50, stock=10)
        Product.objects.create(name="Pear", price=0.75, stock=20)

        # Define endpoints
        self.list_url = '/api/shop/products/'  
        first = Product.objects.first()
        self.detail_url = f'/api/shop/products/{first.pk}/'

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_list_products_public(self):
        """Anyone can list products"""
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 2)

    def test_retrieve_product_public(self):
        """Anyone can retrieve a single product"""
        resp = self.client.get(self.detail_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('name', resp.data)

    def test_create_requires_authentication(self):
        """POST without auth header returns 401"""
        data = {"name": "Banaan", "price": 1.00}
        resp = self.client.post(self.list_url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_product_not_allowed_for_normal_user(self):
        """Authenticated normal user cannot create product"""
        self.authenticate()
        data = {"name": "Banaan", "price": 1.00, "stock": 5}
        resp = self.client.post(self.list_url, data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_create_product_allowed_for_admin(self):
        """Admin user can create product"""
        # Promote user to admin
        self.user.is_staff = True
        self.user.save()
        self.authenticate()
        data = {"name": "Banaan", "price": 1.00, "stock": 5, "description": "Very tasty banana"}
        resp = self.client.post(self.list_url, data, format='json')
        print("ADMIN CREATE ERRORS:", resp.data)

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 3)

    def test_update_requires_authentication(self):
        """PUT/PATCH without auth returns 401"""
        update_data = {"price": 0.99}
        resp = self.client.patch(self.detail_url, update_data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_forbidden_for_normal_user(self):
        """Authenticated normal user cannot update product"""
        self.authenticate()
        resp = self.client.patch(self.detail_url, {"price": 0.99}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_allowed_for_admin(self):
        """Admin user can partially update a product"""
        self.user.is_staff = True
        self.user.save()
        self.authenticate()
        resp = self.client.patch(self.detail_url, {"price": 0.99}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        product = Product.objects.get(pk=Product.objects.first().pk)
        self.assertEqual(float(product.price), 0.99)

    def test_delete_requires_authentication(self):
        """DELETE without auth returns 401"""
        resp = self.client.delete(self.detail_url)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_forbidden_for_normal_user(self):
        """Authenticated normal user cannot delete product"""
        self.authenticate()
        resp = self.client.delete(self.detail_url)
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_allowed_for_admin(self):
        """Admin user can delete a product"""
        self.user.is_staff = True
        self.user.save()
        self.authenticate()
        resp = self.client.delete(self.detail_url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 1)

    def test_invalid_product_data(self):
        """Creation with invalid data returns 400"""
        self.user.is_staff = True
        self.user.save()
        self.authenticate()
        # Test missing name, negative price, missing stock, missing description
        resp = self.client.post(self.list_url, {"name": "", "price": -1, "stock": None, "description": ""}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', resp.data)
        self.assertIn('price', resp.data)
        self.assertIn('stock', resp.data)
        self.assertIn('description', resp.data)
