from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound

from users.models import Address, CustomerProfile
from users.serializers import AddressSerializer, UserProfileSerializer, UserSerializer


class MeProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return self.request.user.profile
        except CustomerProfile.DoesNotExist:
            raise NotFound("No profile has been created for this user yet.")


class MeAddressListCreateView(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]
    # Spectacular does not support empty queryset
    queryset = Address.objects.none()

    def get_queryset(self):
        return Address.objects.filter(profile__user=self.request.user).order_by("id")

    def perform_create(self, serializer):
        profile, _ = CustomerProfile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)


@extend_schema(request=None, responses={204: None})
class MeDeleteView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

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
