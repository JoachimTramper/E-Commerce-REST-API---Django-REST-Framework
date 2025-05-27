from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.addresses import AddressViewSet
from .views.otp import (
    CustomTokenObtainPairView,
    TOTPDisableView,
    TOTPSetupView,
    TOTPVerifyView,
)
from .views.profiles import CustomerProfileViewSet
from .views.users import UserViewSet

app_name = "users"

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"profiles", CustomerProfileViewSet, basename="profiles")
router.register(r"addresses", AddressViewSet, basename="addresses")

urlpatterns = [
    path("", include(router.urls)),
    path("2fa/setup/", TOTPSetupView.as_view(), name="2fa-setup"),
    path("2fa/verify/", TOTPVerifyView.as_view(), name="2fa-verify"),
    path("2fa/", TOTPDisableView.as_view(), name="2fa-disable"),
    path(
        "auth/jwt/create/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
]
