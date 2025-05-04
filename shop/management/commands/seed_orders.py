import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.utils import timezone
from shop.models import Order, OrderItem, Product
from users.models import CustomerProfile


class Command(BaseCommand):
    help = "Seed the database with random orders and order items"

    def handle(self, *args, **options):
        fake = Faker()
        profiles = list(CustomerProfile.objects.all())
        products = list(Product.objects.all())
        statuses = [choice.value for choice in Order.StatusChoices]
        NUM_ORDERS = 200

        total_orders = 0
        total_items = 0

        for _ in range(NUM_ORDERS):
            profile = random.choice(profiles)
            user = profile.user
            order = Order.objects.create(
                user=user,
                status=random.choice(statuses),
            )
            total_orders += 1
            # Generate between 1 and 5 items per order
            for prod in random.sample(products, k=random.randint(1, 5)):
                qty = random.randint(1, 3)
                OrderItem.objects.create(
                    order=order,
                    product=prod,
                    quantity=qty,
                )
                total_items += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"✅ Seeded {total_orders} orders with {total_items} total items."
            )
        )
