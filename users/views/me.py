from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound

from users.models import Address, CustomerProfile
from users.serializers import AddressSerializer, UserProfileSerializer


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

    def get_queryset(self):
        return Address.objects.filter(profile__user=self.request.user).order_by("id")

    def perform_create(self, serializer):
        profile, _ = CustomerProfile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)


class MeDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_destroy(self, instance):
        # soft delete
        instance.is_active = False
        instance.save()
