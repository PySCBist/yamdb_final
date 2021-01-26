from django.contrib.auth.models import AbstractUser
from django.db import models


class Profile(AbstractUser):
    class RoleTypes(models.TextChoices):
        ADMIN = 'admin'
        MODERATOR = 'moderator'
        USER = 'user'

    first_name = models.CharField(max_length=100, blank=True,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=100, blank=True,
                                 verbose_name='Фамилия')
    username = models.CharField(max_length=100, unique=True, primary_key=True,
                                verbose_name='Псевдоним')
    bio = models.TextField(blank=True,
                           verbose_name='О себе')
    email = models.EmailField(unique=True, verbose_name='Почта')
    role = models.CharField(max_length=20, choices=RoleTypes.choices,
                            default=RoleTypes.USER,
                            verbose_name='Тип учётной записи')

    class Meta:
        ordering = ['username', 'role']
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    @property
    def is_admin(self):
        return self.is_superuser or self.role == Profile.RoleTypes.ADMIN

    @property
    def is_moderator(self):
        return self.role == Profile.RoleTypes.MODERATOR
