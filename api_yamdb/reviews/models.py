from django.db import models


# class User(models.Model):
#     pass


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
        related_name='categories',
        on_delete=models.SET_NULL,
    )
    genre = models.ForeignKey(
        Genre,
        null=True,
        blank=True,
        related_name='genres',
        on_delete=models.SET_NULL,
        # many=True
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    pass


class Comment(models.Model):
    pass
