from django.db.models import DecimalField, F, Sum
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from shop.docs.examples import ORDER_EXAMPLES
from shop.filters import OrderFilter
from shop.models import Order
from shop.pagination import FlexiblePageNumberPagination
from shop.permissions import IsOwnerPendingOrAdmin
from shop.serializers import (
    OrderCreateSerializer,
    OrderDetailSerializer,
    OrderListSerializer,
)


@extend_schema(
    request=OrderCreateSerializer,
    responses={
        200: OpenApiResponse(
            response=OrderDetailSerializer, description="Retrieve order"
        ),
        201: OpenApiResponse(
            response=OrderCreateSerializer, description="Create order"
        ),
        400: OpenApiResponse(description="Validation error"),
        404: OpenApiResponse(description="Not found"),
    },
    examples=ORDER_EXAMPLES,
)
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
        if self.action == "list":
            return OrderListSerializer
        if self.action in ("update", "partial_update"):
            return OrderCreateSerializer
        return OrderDetailSerializer

    @action(detail=True, methods=["post"], url_path="checkout")
    def checkout(self, request, pk=None):
        order = self.get_object()
        order.status = Order.StatusChoices.CONFIRMED
        order.save()
        serializer = self.get_serializer(order)
        return Response(serializer.data)

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
