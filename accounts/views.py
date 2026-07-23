from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserSerializer, CustomUserUpdateSerializer, ChangeEmailSerializer


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
        return Response(
            {"message": ("Verification email will be sent to your new email address.")},
            status=status.HTTP_200_OK
        )