from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import permissions, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.throttling import (
    AnonRateThrottle,
    ScopedRateThrottle,
    UserRateThrottle,
)

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
@method_decorator(cache_page(30), name="list")
@method_decorator(cache_page(30), name="retrieve")
class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.select_related("profile", "profile__user").order_by("id")
    serializer_class = AdminAddressSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = FlexiblePageNumberPagination
    throttle_classes = [
        UserRateThrottle,
        AnonRateThrottle,
        ScopedRateThrottle,
    ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["country", "city", "zipcode"]
    search_fields = ["street", "label"]
    ordering_fields = ["country", "city", "id"]
    ordering = ["city"]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminAddressSerializer
        return AddressSerializer

    def get_throttle_scope(self):
        if self.request.method == "GET":
            return "read-burst"
        return "write-burst"
