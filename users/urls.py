# users/urls.py
from rest_framework.routers import DefaultRouter
from .views import CustomerProfileViewSet, AddressViewSet

router = DefaultRouter()
router.register('profiles', CustomerProfileViewSet)
router.register('addresses', AddressViewSet)

urlpatterns = router.urls
