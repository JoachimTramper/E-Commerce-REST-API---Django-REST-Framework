from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Order


class IsOwnerOrAdmin(BasePermission):
    """
    - Admins are always allowed.
    - For safe methods (GET, HEAD, OPTIONS): only owner.
    - For unsafe methods (POST, PUT, PATCH, DELETE): only owner.
    """

    def has_object_permission(self, request, view, obj):
        # 1) Admins always allowed
        if request.user and request.user.is_staff:
            return True

        # 2) Safe methods: only the owner
        if request.method in SAFE_METHODS:
            # veronderstelt dat obj.user de juiste eigenaar is
            return getattr(obj, "user", None) == request.user

        # 3) Non-safe methods: only the owner
        return getattr(obj, "user", None) == request.user


class IsOwnerAndPendingOrAdmin(BasePermission):
    """
    - Admins are always allowed.
    - For SAFE_METHODS (GET, HEAD, OPTIONS): only owner.
    - For DELETE: only owner AND order.status == PENDING.
    - For unsafe methods (POST, PUT, PATCH, DELETE): only owner.
    """

    def has_object_permission(self, request, view, obj):
        # 1) Admins always allowed
        if request.user and request.user.is_staff:
            return True

        # 2) Safe methods: only the owner
        if request.method in SAFE_METHODS:
            return obj.user == request.user

        # 3) DELETE: only owner when status Pending
        if request.method == "DELETE":
            return (
                obj.user == request.user and obj.status == Order.StatusChoices.PENDING
            )

        # 4) Non-safe methods: only the owner
        return obj.user == request.user
