from rest_framework import serializers

from .models import Address, CustomerProfile, User


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "label",
            "street",
            "number",
            "zipcode",
            "city",
            "country",
            "is_billing",
            "is_shipping",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = CustomerProfile
        fields = ["id", "phone_number", "date_of_birth", "addresses"]
        read_only_fields = ["id", "addresses"]


class AdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = ["id", "user", "phone_number", "date_of_birth"]
        extra_kwargs = {
            "user": {"required": True},
        }


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name", "profile"]

        # Unique name for openapi schema generation
        ref_name = "AppUser"


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("email", "username", "password", "first_name", "last_name")

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
        )
        user.is_active = False
        user.save()
        return user
