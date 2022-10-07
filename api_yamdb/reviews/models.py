from django.core.validators import MaxValueValidator, MinValueValidator

from django.db import models

from users.models import User


class Genre(models.Model):
    name = models.TextField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.TextField(max_length=256)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(max_length=16)
    year = models.DateTimeField('year')
    rating = models.IntegerField()
    description = models.TextField(
        null=True,
        blank=True
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        related_name='titles',
        on_delete=models.SET_NULL,
    )
    genre = models.ForeignKey(
        Genre,
        null=True,
        blank=True,
        related_name='titles',
        on_delete=models.SET_NULL,
        # many=True
    )

    def __str__(self):
        return self.name


class Review(models.Model):
#          pass
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE,
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
#     pass
    review_id = models.ForeignKey(Review, on_delete=models.CASCADE,
                                  related_name='comments')
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments', null=True)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True, null=True)
