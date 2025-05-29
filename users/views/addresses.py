from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import permissions, viewsets

from shop.pagination import FlexiblePageNumberPagination
from users.models import Address
from users.serializers import AddressSerializer, AdminAddressSerializer


@extend_schema(
    tags=["users"],
    examples=[
        OpenApiExample(
            "Create address",
            value={
                "label": "Home",
                "street": "Main St",
                "number": "123",
                "zipcode": "12345",
                "city": "Amsterdam",
                "country": "NL",
                "is_billing": True,
                "is_shipping": False,
            },
            request_only=True,
        ),
        OpenApiExample(
            "Address response",
            value={
                "id": 1,
                "label": "Home",
                "street": "Main St",
                "number": "123",
                "zipcode": "12345",
                "city": "Amsterdam",
                "country": "NL",
                "is_billing": True,
                "is_shipping": False,
            },
            response_only=True,
            status_codes=["200", "201"],
        ),
    ],
)
class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all().order_by("id")
    serializer_class = AdminAddressSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = FlexiblePageNumberPagination

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminAddressSerializer
        return AddressSerializer
