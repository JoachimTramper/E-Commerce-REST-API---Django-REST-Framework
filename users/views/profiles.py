from rest_framework import permissions, viewsets

from users.models import CustomerProfile
from users.serializers import AdminProfileSerializer


class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all().order_by("id")
    serializer_class = AdminProfileSerializer
    permission_classes = [permissions.IsAdminUser]
