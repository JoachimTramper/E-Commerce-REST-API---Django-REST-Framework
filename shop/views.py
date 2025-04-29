from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer, OrderItemSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD for Products
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

class OrderViewSet(viewsets.ModelViewSet):
    """
    CRUD for Orders (includes nested read-only items)
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class OrderItemViewSet(viewsets.ModelViewSet):
    """
    CRUD for individual OrderItems (optional in public API)
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]





