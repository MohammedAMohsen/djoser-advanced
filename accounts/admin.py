from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (
            "Profile",
            {
                "fields": (
                    "phone_number",
                    "avatar",
                    "birth_date",
                    "email_verified",
                )
            },
        ),
    )

    list_display = (
        "id",
        "email",
        "username",
        "is_staff",
        "email_verified",
    )

    search_fields = (
        "email",
        "username",
    )