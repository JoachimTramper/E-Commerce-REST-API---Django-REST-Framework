from rest_framework import permissions, viewsets
from rest_framework.exceptions import NotFound

from users.models import Address, CustomerProfile
from users.serializers import AddressSerializer


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(profile__user=self.request.user).order_by("id")

    def perform_create(self, serializer):
        profile, _ = CustomerProfile.objects.get_or_create(user=self.request.user)
        serializer.save(profile=profile)

    def get_object(self):
        obj = super().get_object()
        if obj.profile.user != self.request.user:
            raise NotFound("Address not found.")
        return obj
