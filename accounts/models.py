from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.db import models



class User(AbstractUser):
    email             = models.EmailField(unique=True)
    phone_number      = PhoneNumberField(max_length=20, blank=True, null=True)
    avatar            = models.ImageField(upload_to="users/avatars/", blank=True, null=True)
    birth_date        = models.DateField(blank=True, null=True)
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)
    USERNAME_FIELD    = "email"
    REQUIRED_FIELDS   = ["username"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email