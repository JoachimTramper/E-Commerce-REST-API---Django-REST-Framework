from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.throttling import (
    AnonRateThrottle,
    ScopedRateThrottle,
    UserRateThrottle,
)
from silk.profiling.profiler import silk_profile

from shop.docs.examples import PRODUCT_EXAMPLES
from shop.filters import ProductFilter
from shop.models import Product
from shop.pagination import FlexiblePageNumberPagination
from shop.serializers import ProductSerializer


@extend_schema(
    request=ProductSerializer,
    responses={
        200: OpenApiResponse(
            response=ProductSerializer, description="Retrieve product"
        ),
        201: OpenApiResponse(response=ProductSerializer, description="Create product"),
        400: OpenApiResponse(description="Validation error"),
        404: OpenApiResponse(description="Not found"),
    },
    examples=PRODUCT_EXAMPLES,
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = FlexiblePageNumberPagination

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "name", "stock"]

    throttle_classes = [
        UserRateThrottle,
        AnonRateThrottle,
        ScopedRateThrottle,
    ]

    def get_throttles(self):
        if self.request.method in ("POST", "PUT", "PATCH", "DELETE"):
            self.throttle_scope = "write-burst"
        elif not self.request.user or not self.request.user.is_authenticated:
            self.throttle_scope = "anon"
        else:
            self.throttle_scope = "user"
        return super().get_throttles()

    @method_decorator(cache_page(30))  # cache for 30 seconds
    def list(self, request, *args, **kwargs):
        with silk_profile(name="product-list"):
            return super().list(request, *args, **kwargs)

    @method_decorator(cache_page(60 * 5))  # cache for 5 minutes
    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response["Cache-Control"] = "public, max-age=300"
        return response

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]
