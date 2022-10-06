from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.relations import SlugRelatedField


from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title # Users
)


# class UsersSerializer(serializers.ModelSerializer):
#     pass


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()
    slug = SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Category
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    pass


class GenreSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()
    slug = SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Genre
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    pass


class TitleSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()
    year = serializers.IntegerField()
    rating = serializers.IntegerField(read_only=True)
    description = serializers.CharField(required=False)
    genre = SlugRelatedField(
        slug_field='name',
        many=True,
        queryset=Title.objects.select_related('genres')
    )
    category = SlugRelatedField(
        slug_field='name',
        queryset=Title.objects.select_related('categories')
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')
