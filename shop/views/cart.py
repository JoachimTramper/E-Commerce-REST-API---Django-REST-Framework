from datetime import timedelta

from django.db import transaction
from django.db.models import DecimalField, F, Sum
from django.db.utils import OperationalError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import (
    AnonRateThrottle,
    ScopedRateThrottle,
    UserRateThrottle,
)

from shop.docs.examples import CART_EXAMPLES, CART_ITEM_EXAMPLES
from shop.models import Order, OrderItem, Product
from shop.serializers import (
    CartSerializer,
    OrderItemCreateUpdateSerializer,
    OrderItemDetailSerializer,
    OrderItemListSerializer,
)


@extend_schema_view(
    list=extend_schema(
        request=None,
        responses={
            200: CartSerializer,
            404: OpenApiResponse(description="No pending cart"),
        },
        description="Retrieve the current user's pending cart",
        examples=CART_EXAMPLES,
    ),
    checkout=extend_schema(
        operation_id="cartCheckout",
        request=None,
        responses={
            200: OpenApiResponse(
                description="Stock reserved; you have 10 minutes to complete payment.",
            ),
            400: OpenApiResponse(description="Not enough stock / concurrency error"),
            404: OpenApiResponse(description="No pending cart"),
        },
        description="Reserve stock and sets status to AWAITING_PAYMENT. "
        "Returns 200 + JSON { message: … } if successful.",
    ),
)
class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    throttle_classes = [
        UserRateThrottle,
        AnonRateThrottle,
        ScopedRateThrottle,
    ]
    throttle_scope = "write-burst"

    def list(self, request):
        cart = get_object_or_404(
            Order.objects.prefetch_related("items__product").annotate(
                total_amount=Sum(
                    F("items__quantity") * F("items__price"),
                    output_field=DecimalField(max_digits=12, decimal_places=2),
                )
            ),
            user=request.user,
            status=Order.StatusChoices.PENDING,
        )
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=["post"], url_path="checkout")
    def checkout(self, request):
        """
        When the user checks out:
        1) Retrieve the PENDING order (the cart).
        2) Inside a single transaction, decrement stock for each OrderItem atomically.
           - If stock is insufficient for any product, return an error and roll back.
        3) Only if all stock updates succeed, set the order status to CONFIRMED and save.
        """

        # fetch the pending cart for this user
        cart = get_object_or_404(
            Order.objects.prefetch_related("items__product"),
            user=request.user,
            status=Order.StatusChoices.PENDING,
        )

        expire_at = timezone.now() + timedelta(minutes=10)

        # reserve stock within an atomic transaction
        with transaction.atomic():
            for item in cart.items.all():
                product_id = item.product_id
                qty = item.quantity

                try:
                    # atomically increase stock_reserved if there is enough free stock
                    updated = Product.objects.filter(
                        pk=product_id, stock__gte=F("stock_reserved") + qty
                    ).update(stock_reserved=F("stock_reserved") + qty)
                except OperationalError:
                    # SQLite may raise “table is locked” on concurrent updates
                    return Response(
                        {
                            "detail": f"Could not reserve stock for '{item.product.name}'."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if updated == 0:
                    # not enough available stock to reserve
                    return Response(
                        {
                            "detail": f"Not enough stock to reserve '{item.product.name}'."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            # all items reserved successfully: set reserved_until and status
            cart.reserved_until = expire_at
            cart.status = Order.StatusChoices.AWAITING_PAYMENT
            cart.save()

        # return a simple confirmation message (no real payment in portfolio)
        return Response(
            {"message": "Stock reserved; you have 10 minutes to complete payment."},
            status=status.HTTP_200_OK,
        )


@extend_schema_view(
    list=extend_schema(
        operation_id="cartItemsList",
        responses={200: OrderItemListSerializer(many=True)},
    ),
    retrieve=extend_schema(
        operation_id="cartItemsRetrieve",
        responses={200: OrderItemDetailSerializer()},
    ),
    create=extend_schema(
        operation_id="cartItemCreate",
        request=OrderItemCreateUpdateSerializer,
        responses={201: CartSerializer()},
        examples=CART_ITEM_EXAMPLES,
    ),
    update=extend_schema(
        operation_id="cartItemUpdate",
        request=OrderItemCreateUpdateSerializer,
        responses={200: OrderItemDetailSerializer()},
    ),
    partial_update=extend_schema(
        operation_id="cartItemPartialUpdate",
        request=OrderItemCreateUpdateSerializer,
        responses={200: OrderItemDetailSerializer()},
    ),
    destroy=extend_schema(
        operation_id="cartItemDelete",
        responses={204: OpenApiResponse(description="Cart item deleted")},
    ),
)
class CartItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"
    queryset = OrderItem.objects.none()
    throttle_classes = [
        UserRateThrottle,
        AnonRateThrottle,
        ScopedRateThrottle,
    ]
    throttle_scope = "write-burst"

    def get_queryset(self):
        # only show items from the current user's pending cart
        return OrderItem.objects.select_related("product", "order").filter(
            order__user=self.request.user, order__status=Order.StatusChoices.PENDING
        )

    def get_serializer_class(self):
        if self.action == "list":
            return OrderItemListSerializer
        if self.action in ("create", "update", "partial_update"):
            return OrderItemCreateUpdateSerializer
        return OrderItemDetailSerializer

    def create(self, request, *args, **kwargs):
        # make sure the user has a pending order
        order, _ = Order.objects.get_or_create(
            user=request.user, status=Order.StatusChoices.PENDING
        )

        # add the item to the order
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(order=order)

        # return the updated cart
        return Response(
            CartSerializer(order, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        # only mutate items in a pending order
        item = self.get_object()
        if item.order.status != Order.StatusChoices.PENDING:
            return Response(status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # delete 1 item, last item delete the order
        item = self.get_object()
        order = item.order
        item.delete()
        if not order.items.exists():
            order.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            CartSerializer(order, context={"request": request}).data,
            status=status.HTTP_200_OK,
        )
