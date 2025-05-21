from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Redirect root to Swagger UI
    path("", RedirectView.as_view(url="/api/docs/", permanent=False)),
    # Django admin
    path("admin/", admin.site.urls),
    # JWT via SimpleJWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Browsable API login/logout
    path("api/auth/", include("rest_framework.urls")),
    # Auth-flows via Djoser
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    # Shop and user-app
    path("api/shop/", include(("shop.urls"), namespace="shop")),
    path("api/users/", include(("users.urls"), namespace="users")),
    # API schema and docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui-no-slash",
    ),
]

if settings.DEBUG:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
