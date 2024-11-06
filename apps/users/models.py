from django.contrib.auth.models import AbstractUser
from apps.users.managers import UserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from time import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated at"))

    class Meta:
        abstract = True

    def __str__(self):
        return self.version


class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("student", "Student")
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")
    username = models.CharField(max_length=150, unique=False, null=True, blank=True, verbose_name=_("username"))
    verification_code = models.CharField(max_length=6)
    activation_key_expires = models.DateTimeField(blank=True, null=True)
    email = models.EmailField(max_length=150, unique=True, verbose_name=_("email"))
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.activation_key_expires:
            self.activation_key_expires = timezone.make_naive(self.activation_key_expires)

        super().save(*args, **kwargs)
