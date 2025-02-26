from django.db import models
from django.contrib.auth.models import AbstractUser

from authentication.managers import UserManager

class User(AbstractUser):
    # Use email as the username field for authentication.
    # This custom user model allows for easy extensibility in the future,
    # following best practices for user management.
    email = models.EmailField(unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

