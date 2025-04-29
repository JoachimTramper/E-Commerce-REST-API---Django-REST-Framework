# users/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import CustomerProfile, Address
from .serializers import CustomerProfileSerializer, AddressSerializer

class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    permission_classes = [IsAuthenticated]

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
