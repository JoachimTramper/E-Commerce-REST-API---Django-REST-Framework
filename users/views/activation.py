from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_decode
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from users.tasks import send_welcome_email

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    @action(["post"], detail=False, permission_classes=[AllowAny])
    def activation(self, request, *args, **kwargs):
        response = super().activation(request, *args, **kwargs)

        uid = request.data.get("uid")
        if uid:
            try:
                user_id = urlsafe_base64_decode(uid).decode()
                user = User.objects.get(pk=user_id)
                if user.is_active:
                    send_welcome_email.delay(user.id)
            except Exception as e:
                print("Activation error:", e)
        return response
