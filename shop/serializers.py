from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from .models import Order, OrderItem, Product

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = ["id", "name", "description", "price", "stock", "in_stock", "image"]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value


class OrderItemDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    quantity = serializers.IntegerField()
    item_subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "product_id", "quantity", "item_subtotal"]

    def get_item_subtotal(self, obj) -> Decimal:
        return obj.product.price * obj.quantity

    def validate(self, data):
        qty = data.get("quantity")
        product = data.get("product")
        if qty is None:
            return data

        if qty > product.stock:
            msg = f"You ordered {qty}, but there are only {product.stock} in stock."
            raise serializers.ValidationError({"quantity": msg})

        return data

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value


class OrderItemCreateUpdateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField()
    id = serializers.IntegerField(read_only=True)
    order = serializers.UUIDField(source="order.order_id", read_only=True)
    item_subtotal = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["id", "order", "product", "quantity", "item_subtotal"]

    def get_item_subtotal(self, obj) -> Decimal:
        return obj.price * obj.quantity

    def validate(self, data):
        qty = data.get("quantity")
        product = data.get("product")
        if qty is not None and qty <= 0:
            raise serializers.ValidationError(
                {"quantity": "Quantity must be at least 1."}
            )

        # Check if the product is in stock
        if qty is not None and product is not None and qty > product.stock:
            raise serializers.ValidationError(
                {
                    "quantity": f"You ordered {qty}, but there are only {product.stock} in stock."
                }
            )

        return data

    def create(self, validated_data):
        user = self.context["request"].user

        # try to collect the pending order
        try:
            pending = Order.objects.get(user=user, status=Order.StatusChoices.PENDING)
        except Order.DoesNotExist:
            # if there is no pending order, return 403
            raise PermissionDenied("Cannot add items: no pending order exists.")

        # Otherwise, create the order item
        return OrderItem.objects.create(
            order=pending,
            product=validated_data["product"],
            quantity=validated_data["quantity"],
            price=validated_data["product"].price,
        )


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = ["order_id", "status", "items"]
        extra_kwargs = {
            "order_id": {"read_only": True},
            "user": {"read_only": True},
        }

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        user = self.context["request"].user
        # Transaction atomic block to ensure all-or-nothing
        with transaction.atomic():
            order = Order.objects.create(user=user, **validated_data)
            for item in items_data:
                OrderItem.objects.create(
                    order=order,
                    product=item["product"],
                    quantity=item["quantity"],
                )
        return order

    def update(self, instance, validated_data):
        # Take nested items out or for a PATCH request None
        items_data = validated_data.pop("items", None)

        # Transaction atomic block to ensure all-or-nothing
        with transaction.atomic():
            # Update the order instance
            instance = super().update(instance, validated_data)

            # If items_data is provided, update the order items
            if items_data is not None:
                instance.items.all().delete()
                for item in items_data:
                    OrderItem.objects.create(
                        order=instance,
                        product=item["product"],
                        quantity=item["quantity"],
                    )

        # Commit, otherwise rollback
        return instance


class OrderDetailSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    items = OrderItemDetailSerializer(many=True)
    status = serializers.ChoiceField(
        read_only=True, choices=Order.StatusChoices.choices
    )
    total_amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "order_id",
            "order_number",
            "user",
            "created_at",
            "status",
            "items",
            "total_amount",
        ]
        read_only_fields = [
            "order_id",
            "order_number",
            "created_at",
            "status",
            "total_amount",
        ]

    def validate(self, attrs):
        # Make sure there is at least one item in the order
        items = attrs.get("items") or []
        if not items:
            raise serializers.ValidationError(
                {"items": "Order must contain at least one item."}
            )
        return attrs

    def get_total_amount(self, obj) -> Decimal:
        return obj.total_amount

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItemDetailSerializer().create({**item_data, "order": order})
        return order


class OrderItemListSerializer(serializers.ModelSerializer):
    order = serializers.UUIDField(source="order.order_id", read_only=True)
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    product_name = serializers.CharField(source="product.name", read_only=True)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    item_subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "product",
            "product_name",
            "quantity",
            "price",
            "item_subtotal",
        ]

    def get_item_subtotal(self, obj) -> Decimal:
        return obj.price * obj.quantity


class OrderListSerializer(serializers.ModelSerializer):
    items = OrderItemListSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "order_id",
            "order_number",
            "created_at",
            "status",
            "items",
            "total_amount",
        ]
        read_only_fields = fields

    def get_total_amount(self, obj):
        return obj.total_amount


class CartSerializer(serializers.ModelSerializer):
    items = OrderItemDetailSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = [
            "order_id",
            "created_at",
            "items",
            "total_amount",
        ]
        read_only_fields = fields

    def get_total_amount(self, obj) -> Decimal:
        return obj.total_amount
