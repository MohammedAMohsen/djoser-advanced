from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User Model.

    We inherit from Django's AbstractUser to keep all built-in
    authentication features while allowing future customization.
    """

    pass
