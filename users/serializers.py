from django.contrib.auth import get_user_model
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Address, CustomerProfile

User = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
    # minimal validation for address fields
    zipcode = serializers.CharField(
        required=True,
        min_length=3,
        error_messages={
            "blank": "Zipcode can not be blank.",
            "min_length": "Zipcode has to be at least 3 characters long.",
        },
    )

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


class AdminAddressSerializer(serializers.ModelSerializer):
    # Admins can set the profile directly
    profile = serializers.PrimaryKeyRelatedField(queryset=CustomerProfile.objects.all())

    class Meta:
        model = Address
        fields = [
            "id",
            "profile",
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
    phone_number = serializers.RegexField(
        regex=r"^\d+$",
        required=False,
        allow_blank=True,
        error_messages={"invalid": "Phone number must be numeric."},
    )

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
    # explicitly declare email as EmailField so DRF valideert at PATCH
    email = serializers.EmailField(required=False)
    username = serializers.CharField(required=False, allow_blank=False)

    class Meta:
        model = User
        fields = ["id", "email", "username", "first_name", "last_name", "profile"]
        read_only_fields = ["id"]

        # unique name for openapi schema generation
        ref_name = "AppUser"

    def validate_username(self, value):
        if value == "":
            raise serializers.ValidationError("This field may not be blank.")
        return value

    def update(self, instance, validated_data):
        if "email" in validated_data:
            instance.email = validated_data["email"]
        if "username" in validated_data:
            instance.username = validated_data["username"]
        # first_name and last_name are optional
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        instance.save()
        return instance


class AdminUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "is_active",
            "is_staff",
        ]

    def create(self, validated_data):
        pw = validated_data.pop("password", None)
        user = super().create(validated_data)
        if pw:
            user.set_password(pw)
            user.save()
        return user

    def update(self, instance, validated_data):
        pw = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if pw:
            user.set_password(pw)
            user.save()
        return user


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


class TOTPSetupSerializer(serializers.Serializer):
    qr_code = serializers.CharField(read_only=True)
    secret = serializers.CharField(read_only=True)


class TOTPVerifySerializer(serializers.Serializer):
    token = serializers.CharField(max_length=6)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    def validate(self, attrs):
        # super() checks email+password and sets self.user
        data = super().validate(attrs)

        # add 2fa flag to the response
        user = self.user
        data["has_2fa"] = TOTPDevice.objects.filter(user=user, confirmed=True).exists()
        return data


class EmailTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Invalid credentials", code="authentication"
            )

        if not user.check_password(password):
            raise serializers.ValidationError(
                "Invalid credentials", code="authentication"
            )

        attrs["user"] = user
        return attrs
