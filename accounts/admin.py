from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


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
                    "pending_email",
                )
            },
        ),
    )

    list_display = (
        "id",
        "email",
        "username",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "email",
        "username",
    )
    

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user__username",
        "bio"
    )