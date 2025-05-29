from rest_framework import permissions, viewsets

from users.models import User
from users.serializers import AdminUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = AdminUserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        # Only return active users
        return User.objects.filter(is_active=True).order_by("id")

    def perform_destroy(self, instance):
        # Soft delete: deactivate instead of hard delete
        instance.is_active = False
        instance.save()
