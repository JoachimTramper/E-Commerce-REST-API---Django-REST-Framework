import random
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from shop.models import Order, OrderItem, Product


class Command(BaseCommand):
    help = "Seed orders with max 1 'Pending' per user, plus extra random orders"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        users = list(User.objects.all())
        products = list(Product.objects.all())

        if not users or not products:
            self.stdout.write(self.style.ERROR("❌ Geen users of producten gevonden."))
            return

        created_orders = 0

        # 🔹 1. Geef de helft van de users één 'Pending' order
        pending_users = random.sample(users, len(users) // 2)
        for user in pending_users:
            self._create_order(user, "Pending", products)
            created_orders += 1

        # 🔹 2. Maak extra random orders met andere statussen
        extra_statuses = ["Confirmed", "Shipped", "Delivered", "Cancelled"]
        for _ in range(100):
            user = random.choice(users)
            status = random.choice(extra_statuses)
            self._create_order(user, status, products)
            created_orders += 1

        self.stdout.write(self.style.SUCCESS(f"✅ {created_orders} orders aangemaakt."))

    def _create_order(self, user, status, products):
        order = Order.objects.create(user=user, status=status)

        num_items = random.randint(2, 4)
        selected_products = random.sample(products, min(num_items, len(products)))

        for product in selected_products:
            quantity = random.randint(1, 3)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
            )
