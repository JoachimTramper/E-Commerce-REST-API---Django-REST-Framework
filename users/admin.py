from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import Address, CustomerProfile

User = get_user_model()


@admin.register(User)
class UserAdmin(SimpleHistoryAdmin, BaseUserAdmin):
    """
    Combines Django’s built-in UserAdmin with simple_history,
    so admins get a “History” tab on each User record.
    """

    pass


@admin.register(CustomerProfile)
class CustomerProfileAdmin(SimpleHistoryAdmin):
    list_display = ("user", "phone_number", "date_of_birth")
    search_fields = ("user__email", "phone_number")
    list_filter = ("date_of_birth",)


@admin.register(Address)
class AddressAdmin(SimpleHistoryAdmin):
    list_display = ("profile", "label", "street", "city", "is_billing", "is_shipping")
    list_filter = ("is_billing", "is_shipping")
