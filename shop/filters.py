import django_filters
from django.db.models import F, Sum

from .models import Order, OrderItem, Product


class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    in_stock = django_filters.BooleanFilter(method="filter_in_stock")
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Product
        fields = []  # no default filters

    def filter_in_stock(self, queryset, name, value):
        return queryset.filter(stock__gt=0) if value else queryset.filter(stock__lte=0)


class OrderFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(lookup_expr="iexact")
    created_after = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="gte"
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at", lookup_expr="lte"
    )
    total_min = django_filters.NumberFilter(method="filter_total_min")
    total_max = django_filters.NumberFilter(method="filter_total_max")

    class Meta:
        model = Order
        fields = []

    def filter_total_min(self, qs, name, value):
        # calculate the total price of the order by price * quantity of each item
        return qs.annotate(total=Sum(F("items__price") * F("items__quantity"))).filter(
            total__gte=value
        )

    def filter_total_max(self, qs, name, value):
        return qs.annotate(total=Sum(F("items__price") * F("items__quantity"))).filter(
            total__lte=value
        )


class OrderItemFilter(django_filters.FilterSet):
    order = django_filters.UUIDFilter(field_name="order__order_id", lookup_expr="exact")
    product = django_filters.NumberFilter(field_name="product_id", lookup_expr="exact")
    quantity_min = django_filters.NumberFilter(field_name="quantity", lookup_expr="gte")
    quantity_max = django_filters.NumberFilter(field_name="quantity", lookup_expr="lte")

    class Meta:
        model = OrderItem
        fields = []
