from django.db import models
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    user_info = models.TextField(
        verbose_name='Информация о пользователе'
        )
