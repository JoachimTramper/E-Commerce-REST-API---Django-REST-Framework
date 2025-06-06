from django.conf import settings
from django.db import transaction
from django.db.models import F
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from shop.models import Order, Product
from shop.serializers import PaymentWebhookSerializer
from shop.tasks import send_order_email_with_invoice


@extend_schema(
    operation_id="paymentWebhook",
    parameters=[
        OpenApiParameter(
            name="X-Webhook-Key",
            type=OpenApiTypes.STR,
            location=OpenApiParameter.HEADER,
            description="Secret key required to authenticate the webhook request",
            required=True,
        )
    ],
    request=PaymentWebhookSerializer,
    examples=[
        OpenApiExample(
            name="PaymentWebhookRequest",
            summary="Example payload for payment_webhook",
            value={
                "order_id": "327a8ead-4e5f-4815-a6ed-0ff3ba4d335b",
                "status": "paid",
            },
            request_only=True,
        ),
    ],
    responses={
        200: OpenApiResponse(
            description="Webhook received; if status='paid' and order was AWAITING_PAYMENT, "
            "stock is decremented, order set to CONFIRMED, and invoice email triggered."
        ),
        400: OpenApiResponse(description="Missing data or insufficient stock"),
        403: OpenApiResponse(description="Unauthorized (invalid X-Webhook-Key)"),
        404: OpenApiResponse(description="Order not found"),
    },
    description=(
        "Payment provider callback endpoint:\n"
        "- Verify header `X-Webhook-Key` matches the configured secret.\n"
        "- Expect JSON body with `order_id` (UUID) and `status` ('paid' or 'failed').\n"
        "- If `status == 'paid'` and order is in `AWAITING_PAYMENT`, then:\n"
        "  1) Decrement `stock` and `stock_reserved` for each OrderItem within"
        "     an atomic transaction.\n"
        "  2) Change order status to `CONFIRMED` and save.\n"
        "  3) Dispatch Celery task `send_order_email_with_invoice.delay(order_id)`.\n"
        "- Always return 200 OK with a JSON confirmation message "
        "  `{ 'message': 'Webhook received' }`."
    ),
)
@api_view(["POST"])
def payment_webhook(request):
    """
    Simulate payment provider callback: receive { order_id, status }.
    If status == "paid" and order is in AWAITING_PAYMENT,
    then definitively decrement stock, decrease stock_reserved,
    mark order as CONFIRMED, and send invoice email.
    """

    secret_key = request.headers.get("X-Webhook-Key")
    if secret_key != settings.WEBHOOK_SECRET_KEY:
        return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

    data = request.data
    order_id = data.get("order_id")
    payment_status = data.get("status")

    if not order_id or not payment_status:
        return Response({"error": "Missing data"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        order = Order.objects.get(order_id=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

    if (
        payment_status == "paid"
        and order.status == Order.StatusChoices.AWAITING_PAYMENT
    ):
        with transaction.atomic():
            # definitively deduct from stock and release the reservation
            for item in order.items.all():
                Product.objects.filter(pk=item.product_id).update(
                    stock=F("stock") - item.quantity,
                    stock_reserved=F("stock_reserved") - item.quantity,
                )
            order.status = Order.StatusChoices.CONFIRMED
            order.save()
            # trigger invoice email now that order is confirmed
            send_order_email_with_invoice.delay(str(order.order_id))

    return Response({"message": "Webhook received"}, status=status.HTTP_200_OK)
