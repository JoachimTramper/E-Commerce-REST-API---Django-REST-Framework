from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Order, OrderItem


class IsOwnerPendingOrAdmin(BasePermission):
    """
    - Not logged in: 401 UNAUTHORIZED.
    - Admins are always allowed.
    - For SAFE_METHODS (GET, HEAD, OPTIONS): only owner.
    - For DELETE: only owner AND order.status == PENDING.
    - For unsafe methods (POST, PUT, PATCH, DELETE): only owner.
    """

    def has_permission(self, request, view):
        # 401: only logged-in users are allowed
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated()
        return True

    def has_object_permission(self, request, view, obj):
        # admin always allowed
        if request.user.is_staff:
            return True

        # determine owner and status
        if isinstance(obj, OrderItem):
            owner = obj.order.user
            status_ = obj.order.status
        else:  # obj is Order
            owner = obj.user
            status_ = obj.status

        # SAFE_METHODS (GET, HEAD, OPTIONS): only owner
        if request.method in SAFE_METHODS:
            return owner == request.user

        # DELETE: owner + pending-status (obj can be Order or OrderItem)
        if request.method == "DELETE":
            return owner == request.user and status_ == Order.StatusChoices.PENDING

        # other writes (POST, PUT, PATCH): only owner
        return owner == request.user
