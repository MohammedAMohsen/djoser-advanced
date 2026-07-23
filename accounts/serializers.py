from datetime import date
from djoser.serializers import UserCreateSerializer, UserSerializer, UserCreatePasswordRetypeSerializer
from rest_framework import serializers
from .validators import validate_username,validate_email,validate_birth_date, validate_avatar
from .models import User
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from .tokens import email_change_token_generator


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


class ConfirmEmailChangeSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    default_error_messages = {
        "invalid_link": "Invalid or expired confirmation link.",
        "no_pending_email": "No pending email change request found.",
    }
    def validate(self, attrs):
        try:
            uid = force_str(urlsafe_base64_decode(attrs["uid"]))
            user = User.objects.get(pk=uid)
        except Exception:
            self.fail("invalid_link")
        if not email_change_token_generator.check_token(user,attrs["token"],):
            self.fail("invalid_link")
        if not user.pending_email:
            self.fail("no_pending_email")
        attrs["user"] = user
        return attrs