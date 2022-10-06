from django.contrib.auth.models import AbstractUser
from django.db import models

ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор')
)


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль', max_length=30, choices=ROLE_CHOICES, default='user'
    )
    email = models.EmailField(
        'Email', max_length=254, unique=True, blank=False
    )
    confirmation_code = models.TextField('Код подтверждения', null=True)
