from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .tasks import send_email_task
from .services import build_email_change_confirmation_link
from .serializers import (
    CustomUserSerializer,
    CustomUserUpdateSerializer,
    ChangeEmailSerializer,
    ConfirmEmailChangeSerializer,
    LogoutSerializer,
)


class CustomUserViewSet(UserViewSet):
    def get_serializer_class(self):
        if self.action == "me":
            if self.request.method in ["PATCH", "PUT"]:
                return CustomUserUpdateSerializer
            return CustomUserSerializer
        return super().get_serializer_class()
    
    @action(detail=False, methods=["post"], url_path="change-email")
    def change_email(self, request):
        serializer = ChangeEmailSerializer(data=request.data,context={"request": request},)
        serializer.is_valid(raise_exception=True)
        request.user.pending_email = serializer.validated_data["email"]
        request.user.save(update_fields=["pending_email"])
        confirmation_url = build_email_change_confirmation_link(request.user)
        send_email_task.delay(confirmation_url, request.user.pending_email)
        return Response(
            {"message": ("Verification email will be sent to your new email address.")},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=["post"], permission_classes=[], authentication_classes=[], url_path="confirm-email-change",)
    def confirm_email_change(self, request):
        serializer = ConfirmEmailChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if User.objects.filter(email=user.pending_email).exclude(pk=user.pk).exists():
            return Response(
                {
                    "detail":
                    "Email already exists."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user.email = user.pending_email
        user.pending_email = None
        
        user.save(update_fields=["email", "pending_email",])
        return Response(
            {
            "message":
            "Email changed successfully. Please login again."
            }
        ) # Then Frontend: delete tokens - redirect login
    
    @action(detail=False, methods=["post"], url_path="logout")
    def logout(self, request):
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message":
                "Successfully logged out."
            },
            status=status.HTTP_205_RESET_CONTENT
        )