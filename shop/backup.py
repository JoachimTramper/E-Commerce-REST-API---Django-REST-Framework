from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Product, Order, OrderItem

User = get_user_model()

class ProductSerializer(serializers.ModelSerializer):
    in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock', 'in_stock', 'image'
        ]

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source='product', write_only=True
    )
    item_subtotal = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_id', 'quantity', 'item_subtotal'
        ]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    items = OrderItemSerializer(many=True)
    total_amount = serializers.DecimalField(
        max_digits=12, decimal_places=2, read_only=True
    )
    status = serializers.ChoiceField(choices=Order.StatusChoices.choices, default='Pending')

    class Meta:
        model = Order
        fields = [
            'order_id', 'order_number', 'user', 
            'created_at', 'status', 'items', 'total_amount'
        ]
        read_only_fields = ['order_id', 'order_number', 'created_at', 'total_amount']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data.setdefault('status', 'Pending')  # default status
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Allow status updates only
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
