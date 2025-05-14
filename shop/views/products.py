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
    throttle_scope = "read-burst"

    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        response["Cache-Control"] = "public, max-age=300"
        return response

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]
