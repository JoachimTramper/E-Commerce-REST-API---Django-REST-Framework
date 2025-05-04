from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from .filters import OrderFilter, OrderItemFilter, ProductFilter
from .models import Order, OrderItem, Product
from .pagination import FlexiblePageNumberPagination
from .permissions import IsOwnerAndPendingOrAdmin
from .serializers import (
    OrderCreateSerializer,
    OrderDetailSerializer,
    OrderItemDetailSerializer,
    OrderItemListSerializer,
    OrderListSerializer,
    ProductSerializer,
)


# Products: everyone can see, only staff can create/update/delete
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = FlexiblePageNumberPagination

    # Filtering, searching & ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "name", "stock"]

    def get_permissions(self):
        # list/retrieve → open for everyone
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        # create/update/delete, staff only
        return [IsAdminUser()]


# Orders: logged-in users can create/view their own orders, staff can view all orders
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by("-created_at")
    pagination_class = FlexiblePageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OrderFilter
    search_fields = ["status", "customer__username"]
    ordering_fields = ["created", "total"]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    def get_serializer_class(self):
        # create/update/partial_update, uses writer-serializer
        if self.action in ("create", "update", "partial_update"):
            return OrderCreateSerializer
        if self.action == "list":
            return OrderListSerializer  # compact list‐serializer
        return OrderDetailSerializer  # detailed view‐serializer

    def get_permissions(self):
        # create/list/retrieve, open for logged-in users
        if self.action in ("create", "list", "retrieve"):
            return [IsAuthenticated()]
        if self.action == "destroy":
            # delete, only if the order is pending and the user is the owner or staff
            return [IsOwnerAndPendingOrAdmin()]
        # update/partial_update/destroy, staff only
        return [IsAdminUser()]

    def perform_create(self, serializer):
        # link the order to the logged-in user
        serializer.save()


# OrderItems: same as orders, but staff can see all items
class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    pagination_class = FlexiblePageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OrderItemFilter
    search_fields = ["product__name"]
    ordering_fields = ["quantity", "price"]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(order__user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderItemListSerializer  # compact list‐serializer
        return OrderItemDetailSerializer  # detailed view‐serializer

    def get_permissions(self):
        # list/retrieve, open for logged-in users
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        # create/update/delete, staff only
        return [IsAdminUser()]
