from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import permissions, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.throttling import (
    AnonRateThrottle,
    ScopedRateThrottle,
    UserRateThrottle,
)

from users.models import User
from users.serializers import AdminUserSerializer


@extend_schema(
    tags=["users"],
    parameters=[
        OpenApiParameter(
            "is_active", type=bool, description="Filter on active users (true/false)"
        ),
        OpenApiParameter(
            "is_staff", type=bool, description="Filter on staff users (true/false)"
        ),
        OpenApiParameter(
            "search", type=str, description="Partial search on email or username"
        ),
        OpenApiParameter(
            "ordering",
            type=str,
            description='Sort by date_joined or email; prefix "-" for descending',
        ),
    ],
)
@method_decorator(cache_page(60), name="list")
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAdminUser]
    throttle_classes = [
        UserRateThrottle,
        AnonRateThrottle,
        ScopedRateThrottle,
    ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_active", "is_staff", "email", "date_joined"]
    search_fields = ["email", "username"]
    ordering_fields = ["date_joined", "email", "username"]
    ordering = ["-date_joined"]

    def get_queryset(self):
        qs = User.objects.all().order_by("id")
        is_active_param = self.request.query_params.get("is_active")
        if is_active_param is not None:
            # filter by is_active if provided, if set to "false" return inactive users
            active_bool = is_active_param.lower() == "true"
            return qs.filter(is_active=active_bool)
        # default: return only active users
        return qs.filter(is_active=True)

    def perform_destroy(self, instance):
        # soft delete: deactivate instead of hard delete
        instance.is_active = False
        instance.save()

    def get_throttle_scope(self):
        if self.request.method == "GET":
            return "read-burst"
        return "write-burst"
