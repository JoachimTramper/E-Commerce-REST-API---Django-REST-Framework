from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.throttling import ScopedRateThrottle, UserRateThrottle

from users.models import Address, CustomerProfile
from users.serializers import AddressSerializer, UserProfileSerializer, UserSerializer


class MeProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [
        UserRateThrottle,
        ScopedRateThrottle,
    ]

    def get_object(self):
        try:
            return self.request.user.profile
        except CustomerProfile.DoesNotExist:
            raise NotFound("No profile has been created for this user yet.")

    def get_throttle_scope(self):
        if self.request.method == "GET":
            return "read-burst"
        return "write-burst"


class MeAddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [
        UserRateThrottle,
        ScopedRateThrottle,
    ]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["is_billing", "is_shipping", "city", "country"]
    search_fields = ["street", "label"]
    ordering_fields = ["city", "zipcode", "id"]
    ordering = ["-id"]
    # Spectacular does not support empty queryset
    queryset = Address.objects.none()

    def get_queryset(self):
        return (
            Address.objects.filter(profile__user=self.request.user)
            .select_related("profile", "profile__user")
            .order_by("id")
        )

    def perform_create(self, serializer):
        profile, _ = CustomerProfile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)

    def get_throttle_scope(self):
        if self.request.method == "GET":
            return "read-burst"
        return "write-burst"


@extend_schema(request=None, responses={204: None})
class MeDeleteView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [
        UserRateThrottle,
        ScopedRateThrottle,
    ]
    throttle_scope = "write-burst"

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        # soft delete
        instance.is_active = False
        instance.save()


class MeAddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Authenticated user to GET, PATCH or DELETE their own address.
    """

    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = "pk"
    throttle_classes = [
        UserRateThrottle,
        ScopedRateThrottle,
    ]

    def get_queryset(self):
        # Filter addresses to only those owned by the requesting user
        return Address.objects.filter(profile__user=self.request.user)

    @extend_schema(responses={200: AddressSerializer})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(request=AddressSerializer, responses={200: AddressSerializer})
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @extend_schema(request=None, responses={204: None})
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_throttle_scope(self):
        if self.request.method == "GET":
            return "read-burst"
        return "write-burst"
