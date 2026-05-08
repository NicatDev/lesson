from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField("telefon", max_length=32, blank=True)

    class Meta:
        verbose_name = "istifadəçi"
        verbose_name_plural = "istifadəçilər"
