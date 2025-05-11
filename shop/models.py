import uuid
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import DecimalField, F, Max, Q, Sum, UniqueConstraint

User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to="products/", blank=True, null=True)

    class Meta:
        ordering = ["pk"]

    @property
    def in_stock(self):
        return self.stock > 0

    def __str__(self):
        return self.name


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = "Pending"
        CONFIRMED = "Confirmed"
        SHIPPED = "Shipped"
        DELIVERED = "Delivered"
        CANCELLED = "Cancelled"

    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.PositiveIntegerField(unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.PENDING
    )
    products = models.ManyToManyField(
        Product, through="OrderItem", related_name="orders"
    )
    _total_amount = None

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            UniqueConstraint(
                fields=["user"],
                condition=Q(status="Pending"),
                name="unique_pending_order_per_user",
            )
        ]

    def __str__(self):
        return f"Order {self.order_number} by {self.user.username}"

    def save(self, *args, **kwargs):
        # set order_number to the next available number if not set
        if self.order_number is None:
            last = (
                Order.objects.aggregate(Max("order_number"))["order_number__max"] or 0
            )
            self.order_number = last + 1
        super().save(*args, **kwargs)

    @property
    def total_amount(self):
        if self._total_amount is not None:
            return self._total_amount

        return (
            self.items.aggregate(
                total=Sum(
                    F("quantity") * F("price"),
                    output_field=DecimalField(max_digits=12, decimal_places=2),
                )
            )["total"]
            or 0
        )

    @total_amount.setter
    def total_amount(self, value):
        # set the total amount directly
        self._total_amount = value


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
    )
    _item_subtotal = None

    def save(self, *args, **kwargs):
        # set price to product price if not set
        if self._state.adding and (self.price == Decimal("0.00")):
            self.price = self.product.price
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["pk"]

    @property
    def item_subtotal(self):
        # if item_subtotal is already set, return it
        if self._item_subtotal is not None:
            return self._item_subtotal
        # fallback: calculate subtotal from price and quantity
        return self.price * self.quantity

    @item_subtotal.setter
    def item_subtotal(self, value):
        # set the item subtotal directly
        self._item_subtotal = value

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.order_id})"
