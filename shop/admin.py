# shop/admin.py
from django.contrib import admin

from .models import Order, OrderItem, Product


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]


admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
