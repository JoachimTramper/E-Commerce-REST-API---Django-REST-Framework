from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.addresses import AddressViewSet
from .views.profiles import CustomerProfileViewSet
from .views.users import UserViewSet

app_name = "users"

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"profiles", CustomerProfileViewSet, basename="profiles")
router.register(r"addresses", AddressViewSet, basename="addresses")

urlpatterns = [
    path("", include(router.urls)),
]
