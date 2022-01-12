from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator


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


class Titles(models.Model):
    name = models.CharField(max_length=50)
    genre = models.ManyToManyField('Genre', through='GenreOfTitle')
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,
                                 null=True, blank=True)
    year = models.IntegerField(
        validators=[MaxValueValidator(timezone.now().year)]
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class GenreTitle(models.Model):
    genre = models.ForeignKey('Genres', on_delete=models.CASCADE)
    title = models.ForeignKey('Titles', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'
