from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core import validators


class User(AbstractUser):
    ROLES = (
        ('admin', 'Администратор'),
        ('moderator', 'Модератор'),
        ('user', 'Пользователь'),
    )
    email = models.EmailField(
        validators=[validators.validate_email],
        unique=True,
        blank=False,
    )
    role = models.CharField(
        'Роль', max_length=20,
        choices=ROLES, default='user'
    )
    bio = models.TextField('Биография', null=True, blank=True)

    def __str__(self):
        return self.username
