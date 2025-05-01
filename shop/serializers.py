from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db import transaction
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
    order       = serializers.PrimaryKeyRelatedField(read_only=True)
    quantity = serializers.IntegerField()
    item_subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_id', 'quantity', 'item_subtotal']

    def get_item_subtotal(self, obj):
        return obj.product.price * obj.quantity

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value


class OrderCreateSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['order_id', 'status', 'items']
        extra_kwargs = {
            'order_id': {'read_only': True},
            'user': {'read_only': True},
        }

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(user=user, **validated_data)

        for item in items_data:
            product = item['product']
            quantity = item['quantity']
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity
            )

        return order
    
    def update(self, instance, validated_data):
        # Take nested items out or for a PATCH request None
        items_data = validated_data.pop('items', None)

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
                        product=item['product'],
                        quantity=item['quantity']
                    )

        # Commit, otherwise rollback
        return instance
    

class OrderSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()
    status = serializers.ChoiceField(
        choices=Order.StatusChoices.choices,
        read_only=True
    )

    class Meta:
        model = Order
        fields = [
            'order_id', 'order_number', 'user',
            'created_at', 'status', 'items', 'total_amount'
        ]

    def get_total_amount(self, obj):
        return obj.total_amount
