from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from api_yamdb.settings import ATTENTION_RESERVED_NAME, RESERVED_NAME


class CustomUserManager(UserManager):
    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Заполнять поле email обязательно')
        if username == RESERVED_NAME:
            raise ValueError(ATTENTION_RESERVED_NAME)
        return super().create_user(
            username, email=email, password=password, **extra_fields)

    def create_superuser(
            self, username, email, password, role='admin', **extra_fields):
        return super().create_superuser(
            username, email, password, role='admin', **extra_fields)


class User(AbstractUser):
    ROLE = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )
    role = models.CharField(max_length=150, choices=ROLE, default='user')
    username = models.CharField(max_length=150, unique=True)
    bio = models.TextField('bio', blank=True)
    email = models.EmailField(max_length=254, unique=True)
    objects = CustomUserManager()

    class Meta:
        ordering = ('id', )
        verbose_name_plural = 'users'

    @property
    def is_admin(self):
        return self.role == self.ROLE[2][0]

    @property
    def is_moderator(self):
        return self.role == self.ROLE[1][0]
