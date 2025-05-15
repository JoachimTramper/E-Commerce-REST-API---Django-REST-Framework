from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.address import AddressViewSet
from .views.profile import CustomerProfileViewSet
from .views.user import UserViewSet

app_name = "users"

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"profiles", CustomerProfileViewSet, basename="profiles")
router.register(r"addresses", AddressViewSet, basename="addresses")

urlpatterns = [
    # Djoser basic endpoints: register, activate, password reset, user detail
    path("", include("djoser.urls")),
    # JWT endpoints: /users/jwt/create/, /users/jwt/refresh/, /users/jwt/verify/
    path("", include("djoser.urls.jwt")),
    # Other endpoints
    path("", include(router.urls)),
]
