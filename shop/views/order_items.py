from django.db.models import DecimalField, ExpressionWrapper, F
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated

from shop.docs.examples import ORDER_ITEM_EXAMPLES
from shop.filters import OrderItemFilter
from shop.models import Order, OrderItem
from shop.pagination import FlexiblePageNumberPagination
from shop.permissions import IsOwnerPendingOrAdmin
from shop.serializers import (
    OrderItemCreateUpdateSerializer,
    OrderItemDetailSerializer,
    OrderItemListSerializer,
)


@extend_schema(
    request=OrderItemCreateUpdateSerializer,
    responses={
        200: OpenApiResponse(
            response=OrderItemDetailSerializer, description="Retrieve order-item"
        ),
        201: OpenApiResponse(
            response=OrderItemDetailSerializer, description="Create order-item"
        ),
        400: OpenApiResponse(description="Validation error"),
        404: OpenApiResponse(description="Not found"),
    },
    examples=ORDER_ITEM_EXAMPLES,
)
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
