from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from two_factor.urls import urlpatterns as tf_urls

from shop.views.health import health_check
from shop.views.payments import payment_webhook

urlpatterns = [
    # redirect root to Swagger UI
    path("", RedirectView.as_view(url="/api/docs/", permanent=False)),
    # django admin
    path("admin/", admin.site.urls),
    # JWT via SimpleJWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # browsable API login/logout
    path("api/auth/", include("rest_framework.urls")),
    # auth-flows via Djoser
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.jwt")),
    # two-factor authentication
    path("api/account/", include(tf_urls)),
    # shop and user-app
    path("api/shop/", include(("shop.urls"), namespace="shop")),
    # payment webhook
    path("api/webhooks/payment/", payment_webhook, name="payment-webhook"),
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
    # health check
    path("api/health/", health_check, name="health-check"),
]

if settings.DEBUG:
    urlpatterns += [path("silk/", include("silk.urls", namespace="silk"))]
