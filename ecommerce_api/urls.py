from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),
    # JWT Authentication endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # SessionAuthentication for browsable API login/logout
    path("api/auth/", include("rest_framework.urls")),
    # Shop and user app APIs via router
    path("api/shop/", include(("shop.urls"), namespace="shop")),
    path("api/users/", include(("users.urls"), namespace="users")),
    # API schema generation and documentation
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
