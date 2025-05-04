# users/urls.py
from rest_framework.routers import DefaultRouter

from .views import AddressViewSet, CustomerProfileViewSet, UserViewSet

app_name = "users"  # Namespace for the users app

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"profiles", CustomerProfileViewSet)
router.register(r"addresses", AddressViewSet)

urlpatterns = router.urls
