from datetime import date
from djoser.serializers import UserCreateSerializer, UserSerializer, UserCreatePasswordRetypeSerializer
from rest_framework import serializers
from .validators import validate_username,validate_email,validate_birth_date, validate_avatar
from .models import User


class CustomUserCreateSerializer(UserCreatePasswordRetypeSerializer):
    """
    Custom registration serializer.
    Features:
    - Reserved username validation.
    - Email domain validation.
    - Age validation.
    """
    class Meta(UserCreatePasswordRetypeSerializer.Meta):
        model = User
        fields = (
            "id",
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "phone_number",
            "birth_date",
        )
        
    def validate_username(self, value):
        return validate_username(value)

    def validate_email(self, value):
        return validate_email(value)

    def validate_birth_date(self, value):
        return validate_birth_date(value)


class CustomUserSerializer(UserSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta(UserSerializer.Meta):
        model = User
        fields = (
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "full_name",
            "phone_number",
            "birth_date",
            "avatar",
        )

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


class CustomUserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer responsible only for updating the current user's profile.
    """
    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "birth_date",
            "avatar",
        )

    def validate_username(self, value):
        return validate_username(value)

    def validate_birth_date(self, value):
        return validate_birth_date(value)
    
    def validate_avatar(self, value):
        return validate_avatar(value)
    
    
class ChangeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        value = validate_email(value)
        user = self.context["request"].user
        if value == user.email:
            raise serializers.ValidationError("This is already your current email.")
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        if User.objects.filter(pending_email=value).exists():
            raise serializers.ValidationError("This email is awaiting confirmation by another account.")
        return value