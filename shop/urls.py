from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, OrderViewSet, OrderItemViewSet

app_name = "shop"  # Namespace for the shop app

router = DefaultRouter()
router.register(r"products", ProductViewSet)
router.register(r"orders", OrderViewSet)
router.register(r"order-items", OrderItemViewSet)

urlpatterns = router.urls
