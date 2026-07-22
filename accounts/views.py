from django.shortcuts import render
from djoser.views import UserViewSet
from .serializers import CustomUserSerializer, CustomUserUpdateSerializer
from .utils import success_response
from rest_framework import status


class CustomUserViewSet(UserViewSet):
    def get_serializer_class(self):
        if self.action == "me":
            if self.request.method in ["PATCH", "PUT"]:
                return CustomUserUpdateSerializer
            return CustomUserSerializer
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        """
        Override Djoser's register endpoint response.
        """
        response = super().create(request, *args, **kwargs)
        return success_response(
            data=response.data,
            message="Account created successfully.",
            status_code=status.HTTP_201_CREATED,
        )