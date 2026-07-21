from django.shortcuts import render
from djoser.views import UserViewSet
from .serializers import CustomUserSerializer, CustomUserUpdateSerializer


class CustomUserViewSet(UserViewSet):
    def get_serializer_class(self):
        if self.action == "me":
            if self.request.method in ["PATCH", "PUT"]:
                return CustomUserUpdateSerializer
            return CustomUserSerializer
        return super().get_serializer_class()