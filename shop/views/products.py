from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

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

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [AllowAny()]
        return [IsAuthenticated(), IsAdminUser()]
