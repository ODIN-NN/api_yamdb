from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from django.db import models

from users.models import User


class Category(models.Model):
    name = models.TextField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(max_length=64)
    year = models.IntegerField()
    rating = models.IntegerField(
        null=True,
        blank=True
    )
    description = models.TextField(
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles'
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField(max_length=256)
    slug = models.SlugField(unique=True)
    title = models.ManyToManyField(
        Title,
        related_name='genre'
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE,
                                 related_name='reviews')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='reviews')
    score = models.IntegerField(default=0,
                                blank=True,
                                verbose_name='Рейтинг',
                                validators=[
                                    MaxValueValidator(10),
                                    MinValueValidator(1)
                                ])
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return f'Отзыв о произведении {self.title_id.name}'


class Comment(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE,
                               related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True,
    )
