from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.throttling import (
    AnonRateThrottle,
    ScopedRateThrottle,
    UserRateThrottle,
)

from users.models import CustomerProfile
from users.serializers import AdminProfileSerializer


@method_decorator(cache_page(30), name="list")
@method_decorator(cache_page(30), name="retrieve")
class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.select_related("user").order_by("id")
    serializer_class = AdminProfileSerializer
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [
        UserRateThrottle,
        AnonRateThrottle,
        ScopedRateThrottle,
    ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["phone_number", "date_of_birth"]
    search_fields = ["phone_number"]
    ordering_fields = ["date_of_birth", "id"]
    ordering = ["-date_of_birth"]

    def get_throttle_scope(self):
        if self.request.method == "GET":
            return "read-burst"
        return "write-burst"
