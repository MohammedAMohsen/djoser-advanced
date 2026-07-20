from datetime import date
from djoser.serializers import UserCreateSerializer, UserSerializer, UserCreatePasswordRetypeSerializer
from rest_framework import serializers

from .models import User


class CustomUserCreateSerializer(UserCreatePasswordRetypeSerializer):
    """
    Custom registration serializer.
    Features:
    - Password confirmation.
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
        
    # -----------------------------------------
    # Username Validation
    # -----------------------------------------

    def validate_username(self, value):
        reserved = {
            "admin",
            "administrator",
            "root",
            "superuser",
            "system",
            "support",
        }
        if value.lower() in reserved:
            raise serializers.ValidationError("This username is reserved.")
        return value

    # -----------------------------------------
    # Email Validation
    # -----------------------------------------

    def validate_email(self, value):
        blocked_domains = {
            "mailinator.com",
            "10minutemail.com",
            "tempmail.com",
        }
        domain = value.split("@")[-1].lower()
        if domain in blocked_domains:
            raise serializers.ValidationError("Temporary email addresses are not allowed.")
        return value

    # -----------------------------------------
    # Birth Date Validation
    # -----------------------------------------

    def validate_birth_date(self, value):
        today = date.today()
        age = (
            today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        )
        if age < 18:
            raise serializers.ValidationError("You must be at least 18 years old.")
        return value


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
            "email_verified",
        )

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()