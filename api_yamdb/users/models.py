from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLES = (
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('user', 'Пользователь'),
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
    )
    role = models.CharField(
        'Роль', max_length=20,
        choices=ROLES, default='user',
    )
    bio = models.TextField('Биография', null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.username
