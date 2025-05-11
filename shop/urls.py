from rest_framework.routers import DefaultRouter

from .views import CartViewSet, OrderItemViewSet, OrderViewSet, ProductViewSet
from .views.cart import CartItemViewSet

app_name = "shop"

router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"order-items", OrderItemViewSet, basename="order-items")
router.register(r"cart", CartViewSet, basename="cart")
router.register(r"cart/items", CartItemViewSet, basename="cart-items")

urlpatterns = router.urls
