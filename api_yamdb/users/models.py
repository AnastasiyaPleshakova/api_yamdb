from django.contrib.auth.models import AbstractUser
from django.db import models

FIRST_OBJECT = 0


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
        max_length=254,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Имя пользователя',
        max_length=150,
        unique=True,
    )
    role = models.CharField(
        'Роль', max_length=max([len(role[FIRST_OBJECT]) for role in ROLES]),
        choices=ROLES, default='user',
    )
    bio = models.TextField(
        verbose_name='Биография',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']
        verbose_name = 'Пользователь'

    def __str__(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return (
            self.role == self.ADMIN and
            self.is_superuser and
            self.is_staff
        )
