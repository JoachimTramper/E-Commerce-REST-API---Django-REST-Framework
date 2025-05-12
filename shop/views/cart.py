from django.db.models import DecimalField, F, Sum
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import OpenApiResponse, extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from shop.docs.examples import CART_EXAMPLES, CART_ITEM_EXAMPLES
from shop.models import Order, OrderItem
from shop.serializers import (
    CartSerializer,
    OrderItemCreateUpdateSerializer,
    OrderItemDetailSerializer,
    OrderItemListSerializer,
)


@extend_schema(
    request=None,
    responses={
        200: CartSerializer,
        404: OpenApiResponse(description="No pending cart"),
    },
    description="Retrieve the current user's pending cart",
    examples=CART_EXAMPLES,
)
class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        cart = get_object_or_404(
            Order.objects.annotate(
                total_amount=Sum(
                    F("items__quantity") * F("items__price"),
                    output_field=DecimalField(max_digits=12, decimal_places=2),
                )
            ),
            user=request.user,
            status=Order.StatusChoices.PENDING,
        )
        return Response(CartSerializer(cart).data)


# @extend_schema(
#     request=OrderItemCreateUpdateSerializer,
#     responses={
#         200: OrderItemListSerializer(many=True),
#         201: CartSerializer,
#         400: OpenApiResponse(description="Validation error"),
#         404: OpenApiResponse(description="Not found"),
#     },
#     examples=CART_ITEM_EXAMPLES,
#     methods={
#         'list': extend_schema(operation_id='cartItemsList'),
#         'retrieve': extend_schema(operation_id='cartItemsRetrieve'),
#         'create': extend_schema(operation_id='cartItemCreate'),
#     }
# )
# @extend_schema_view(
#     list=extend_schema(
#         operation_id="cartItemsList",
#         responses={200: OrderItemListSerializer(many=True)},
#     ),
#     retrieve=extend_schema(
#         operation_id="cartItemsRetrieve",
#         responses={200: OrderItemDetailSerializer()},
#     ),
#     create=extend_schema(
#         operation_id="cartItemCreate",
#         request=OrderItemCreateUpdateSerializer,
#         responses={201: CartSerializer()},
#         examples=CART_ITEM_EXAMPLES,
#     ),
# )
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

    def get_queryset(self):
        # Only show items from the current user's pending cart
        return OrderItem.objects.filter(
            order__user=self.request.user, order__status=Order.StatusChoices.PENDING
        )

    def get_serializer_class(self):
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
