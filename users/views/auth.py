# from django.conf import settings
# from django.core.mail import send_mail
# from django.shortcuts import get_object_or_404
# from rest_framework import generics, status
# from rest_framework.response import Response

# from users.models import EmailVerificationToken
# from users.serializers import RegisterSerializer

# class RegisterView(generics.CreateAPIView):
#     serializer_class = RegisterSerializer

#     def perform_create(self, serializer):
#         user = serializer.save()
#         token_obj = EmailVerificationToken.objects.create(user=user)
#         verify_url = f"{settings.FRONTEND_URL}/api/auth/verify-email/?token={token_obj.token}"
#         send_mail(
#             subject="Bevestig je e-mailadres",
#             message=f"Klik op de link om je account te activeren:\n{verify_url}",
#             from_email=settings.DEFAULT_FROM_EMAIL,
#             recipient_list=[user.email],
#         )

# class VerifyEmailView(generics.GenericAPIView):
#     def get(self, request):
#         token = request.query_params.get("token")
#         token_obj = get_object_or_404(EmailVerificationToken, token=token)
#         if token_obj.is_expired:
#             return Response({"detail": "Token verlopen."}, status=status.HTTP_400_BAD_REQUEST)
#         user = token_obj.user
#         user.is_active = True
#         user.save()
#         token_obj.delete()
#         return Response({"detail": "E-mail succesvol geverifieerd."}, status=status.HTTP_200_OK)
