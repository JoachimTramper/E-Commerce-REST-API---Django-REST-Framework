from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, CustomerProfile, Address

# User met default UserAdmin (ondersteunt jouw email-login out of the box)
admin.site.register(User, BaseUserAdmin)
admin.site.register(CustomerProfile)
admin.site.register(Address)