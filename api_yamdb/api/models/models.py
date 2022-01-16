from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True)

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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

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

    def __str__(self):
        return self.username


class Category(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} {self.name}'


class Genre(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name} {self.name}'


class GenreTitle(models.Model):
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    title = models.ForeignKey('Titles', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Titles(models.Model):
    name = models.CharField(max_length=50)
    genre = models.ManyToManyField('Genre', through='GenreTitle',
                                   related_name='category')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 related_name='category')
    year = models.IntegerField(
        validators=[MaxValueValidator(timezone.now().year)]
    )
    description = models.CharField(
        max_length=100, blank=True, null=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
