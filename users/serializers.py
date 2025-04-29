# users/serializers.py
from rest_framework import serializers
from .models import CustomerProfile, Address

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = '__all__'

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'
