from django.conf import settings
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from shop.models import Order


@extend_schema(
    request=None,
    responses={200: OpenApiResponse(description="Webhook received", response=None)},
)
@api_view(["POST"])
def payment_webhook(request):
    # Simple header key check
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

    if payment_status == "paid":
        order.status = Order.StatusChoices.CONFIRMED
        order.save()

    return Response({"message": "Webhook received"}, status=status.HTTP_200_OK)
