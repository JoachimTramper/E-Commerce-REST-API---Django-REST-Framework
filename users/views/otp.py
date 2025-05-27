from io import BytesIO
from urllib.parse import parse_qs, urlparse

import qrcode
import qrcode.image.svg
from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework import generics, permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import (
    EmailTokenSerializer,
    TOTPSetupSerializer,
    TOTPVerifySerializer,
)


class TOTPSetupView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TOTPSetupSerializer

    def get(self, request):
        # delete old, unconfirmed devices
        request.user.totpdevice_set.filter(confirmed=False).delete()

        # create a new TOTPDevice
        device = TOTPDevice.objects.create(user=request.user, confirmed=False)
        uri = device.config_url

        # render QR code as SVG
        img = qrcode.make(uri, image_factory=qrcode.image.svg.SvgImage)
        buffer = BytesIO()
        img.save(buffer)
        qr_svg = buffer.getvalue().decode("utf-8", errors="ignore")

        # parse the Base32 secret from the URI
        parsed = urlparse(uri)
        secret = parse_qs(parsed.query)["secret"][0]

        data = {"qr_code": qr_svg, "secret": secret}
        return Response(data)


class TOTPVerifyView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TOTPVerifySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["token"]

        # check if the user has an unconfirmed TOTPDevice
        try:
            device = request.user.totpdevice_set.get(confirmed=False)
        except TOTPDevice.DoesNotExist:
            return Response(
                {"detail": "No setup in progress"}, status=status.HTTP_400_BAD_REQUEST
            )

        if device.verify_token(token):
            device.confirmed = True
            device.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"token": "Invalid code"}, status=status.HTTP_400_BAD_REQUEST)


class TOTPDisableView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        request.user.totpdevice_set.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(APIView):
    """
    Login view that accepts email and password, returning JWT tokens and a 2FA flag.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = EmailTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "has_2fa": TOTPDevice.objects.filter(user=user, confirmed=True).exists(),
        }
        return Response(data)
