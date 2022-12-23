from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    ROLES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=settings.EMAIL_MAX_LENGTH,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=settings.USERNAME_MAX_LENGTH,
        unique=True,
    )
    role = models.CharField(
        'Роль', max_length=max([len(value) for value, name in ROLES]),
        choices=ROLES, default='user',
    )
    bio = models.TextField(
        'Биография',
        null=True,
        blank=True
    )
    first_name = models.TextField(
        'Имя',
        max_length=settings.USER_NAME_MAX_LENGTH,
        null=True,
        blank=True
    )
    last_name = models.TextField(
        'Фамилия',
        max_length=settings.USER_NAME_MAX_LENGTH,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return (
            self.role == self.ADMIN
            or self.is_superuser
            or self.is_staff
        )
