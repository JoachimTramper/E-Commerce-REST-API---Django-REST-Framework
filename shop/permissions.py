from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Order

class IsOwnerAndPendingOrAdmin(BasePermission):
    """
    Allows deleting if:
      - request.user.is_staff is (admin)
      - OR request.user is the owner AND order.status == PENDING
    """
    def has_object_permission(self, request, view, obj):
        # always allow GET, HEAD or OPTIONS requests
        if request.method in SAFE_METHODS:
            return True

        # admin is always allowed
        if request.user.is_staff:
            return True

        # DELETE: only allowed if the user is the owner and order status is PENDING
        if request.method == 'DELETE':
            return obj.user == request.user and obj.status == Order.StatusChoices.PENDING

        # update/patch: can add logic here if needed
        return False