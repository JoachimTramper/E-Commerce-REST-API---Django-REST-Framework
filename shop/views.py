from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from .filters import OrderFilter, OrderItemFilter, ProductFilter
from .models import Order, OrderItem, Product
from .pagination import FlexiblePageNumberPagination
from .permissions import IsOwnerPendingOrAdmin
from .serializers import (
    OrderCreateSerializer,
    OrderDetailSerializer,
    OrderItemCreateUpdateSerializer,
    OrderItemDetailSerializer,
    OrderItemListSerializer,
    OrderListSerializer,
    ProductSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = FlexiblePageNumberPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "name", "stock"]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]


class OrderItemViewSet(viewsets.ModelViewSet):
    """
    - Admin users: full CRUD on all order items.
    - Non-staff users:
        • list/retrieve: only items from their own orders.
        • create: only if they have at least one PENDING order.
        • update/partial_update: only on items whose order status == PENDING.
        • delete: only on items whose order status == PENDING.
    """

    queryset = OrderItem.objects.select_related("order", "product").annotate(
        item_subtotal=ExpressionWrapper(
            F("price") * F("quantity"),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        )
    )
    permission_classes = [IsAuthenticated, IsOwnerPendingOrAdmin]
    pagination_class = FlexiblePageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OrderItemFilter
    search_fields = ["product__name"]
    ordering_fields = ["quantity", "item_subtotal"]

    def get_queryset(self):
        qs = super().get_queryset()

        # admin sees everything
        if self.request.user.is_staff:
            return qs.order_by("-order__created_at", "id")

        # user sees only their own items
        qs = qs.filter(order__user=self.request.user)

        # show all statuses for admin
        qp = self.request.query_params
        filter_params = {"product", "quantity_min", "quantity_max"}
        if self.action == "list" and any(key in qp for key in filter_params):
            return qs.order_by("-order__created_at", "id")

        # or show only pending items
        if self.action in ("list", "retrieve"):
            qs = qs.filter(order__status=Order.StatusChoices.PENDING)

        # final ordering
        return qs.order_by("-order__created_at", "id")

    def get_serializer_class(self):
        if self.action == "list":
            return OrderItemListSerializer
        if self.action in ("create", "update", "partial_update"):
            return OrderItemCreateUpdateSerializer
        return OrderItemDetailSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    - Admin users: full CRUD on all orders.
    - Non-staff users:
        • list/retrieve: only their own orders.
        • create: may create orders for themselves.
        • update/partial_update: only on their own orders when status == PENDING.
        • delete: only on their own orders when status == PENDING.
    """

    queryset = Order.objects.all().annotate(
        total_amount=Sum(
            F("items__quantity") * F("items__price"),
            output_field=DecimalField(max_digits=12, decimal_places=2),
        )
    )
    permission_classes = [IsAuthenticated, IsOwnerPendingOrAdmin]
    pagination_class = FlexiblePageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = OrderFilter
    search_fields = ["status", "user__username"]
    ordering_fields = ["created_at", "total_amount"]
    lookup_field = "pk"

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs.order_by("-created_at")
        return qs.filter(user=self.request.user).order_by("-created_at")

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return OrderCreateSerializer
        if self.action == "list":
            return OrderListSerializer
        return OrderDetailSerializer

    def perform_create(self, serializer):
        # serializer already has the user from the request
        serializer.save()

    def get_permissions(self):
        # for destroy action, check if the user is authenticated
        if self.action == "destroy":
            return [AllowAny()]
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        # check if user is authenticated
        if not request.user or not request.user.is_authenticated:
            return Response(status=status.HTTP_403_FORBIDDEN)
        # get the order
        order = get_object_or_404(Order, pk=kwargs["pk"])
        # admin always allowed
        if request.user.is_staff:
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # only owner and pending orders can be deleted
        if order.user != request.user or order.status != Order.StatusChoices.PENDING:
            return Response(status=status.HTTP_403_FORBIDDEN)
        # delete the order
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
