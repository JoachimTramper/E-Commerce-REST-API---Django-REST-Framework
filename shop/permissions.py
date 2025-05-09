from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from rest_framework.permissions import SAFE_METHODS, BasePermission

from .models import Order, OrderItem


class IsOwnerPendingOrAdmin(BasePermission):
    """
    - Not logged in → 401 UNAUTHORIZED.
    - Admins always allowed.
    - For OrderViewSet:
       * SAFE_METHODS: only owner
       * DELETE: only owner AND order.status == PENDING
       * other writes: only owner
    - For OrderItemViewSet:
       * create: only if user has a pending Order → else 403
       * list/retrieve: only own items of pending orders
       * update/partial_update/destroy: only own items AND order.status == PENDING
    """

    def has_permission(self, request, view):
        # user must be logged in
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated()

        # check if user has a pending order
        if view.action == "create" and view.get_queryset().model is OrderItem:
            if not Order.objects.filter(
                user=request.user, status=Order.StatusChoices.PENDING
            ).exists():
                raise PermissionDenied("You have no pending order to add items to.")

        # all other actions allowed
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

        # UPDATE / PATCH on Order: alleen owner EN PENDING
        if isinstance(obj, Order) and request.method in ("PUT", "PATCH"):
            return owner == request.user and status_ == Order.StatusChoices.PENDING

        # DELETE: owner + pending-status (obj can be Order or OrderItem)
        if request.method == "DELETE":
            return owner == request.user and status_ == Order.StatusChoices.PENDING

        # UPDATE / PATCH on OrderItem: alleen owner EN pending-status
        if isinstance(obj, OrderItem) and request.method in ("PUT", "PATCH"):
            return owner == request.user and status_ == Order.StatusChoices.PENDING

        # other writes (POST, PUT, PATCH): only owner
        return owner == request.user
