from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('user', 'Пользователь'),
    )
    role = models.CharField('Роль', max_length=20, choices=ROLES, default='user')
    bio = models.TextField('Биография', null=True, blank=True)
