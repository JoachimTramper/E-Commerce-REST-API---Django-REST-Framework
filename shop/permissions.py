from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Order, OrderItem


class IsOwnerPendingOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False  # DRF -> 401 (unauthorized)

        if view.action == "create" and view.basename == "orderitems":
            # no pending order → 403
            return Order.objects.filter(
                user=request.user, status=Order.StatusChoices.PENDING
            ).exists()

        return True

    def has_object_permission(self, request, view, obj):
        # staff always OK
        if request.user.is_staff:
            return True

        # determine owner & status
        if isinstance(obj, OrderItem):
            owner, status = obj.order.user, obj.order.status
        else:
            owner, status = obj.user, obj.status

        # safe methods: only owner
        if request.method in SAFE_METHODS:
            return owner == request.user

        # writes require owner + pending
        return owner == request.user and status == Order.StatusChoices.PENDING
