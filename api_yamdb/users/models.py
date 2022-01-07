from django.contrib.auth.models import AbstractUser
from django.db import models


WRONG_YEAR = 'Указан некорректный год'


class User(AbstractUser):
    email = models.EmailField(unique=True, null=True)

    class RoleList:
        USER = 'user'
        ADMIN = 'admin'
        MODERATOR = 'moderator'
        choices = [
            (USER, 'user'),
            (ADMIN, 'admin'),
            (MODERATOR, 'moderator'),
        ]
    
    role = models.CharField(
        max_length=128,
        choices=RoleList.choices,
        default=RoleList.USER,
    )
    bio = models.TextField(default='')

    @property
    def is_admin(self):
        return (self.role == self.RoleList.ADMIN or self.is_superuser)

    @property
    def is_moderator(self):
        return (self.is_admin or self.role == self.RoleList.MODERATOR)

    def get_payload(self):
        return {
            'user_id': self.id,
            'username': self.username,
            'email': self.email,
        }

    class Meta:
        ordering = ('username',)
        verbose_name = 'User'
        verbose_name_plural = 'Users'
