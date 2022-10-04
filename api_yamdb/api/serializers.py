from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.relations import SlugRelatedField


from reviews.models import Categories, Comments, Genres, Reviews, Title, # Users


# class UsersSerializer(serializers.ModelSerializer):
#     pass


class CategoriesSerializer(serializers.ModelSerializer):
    pass


class CommentsSerializer(serializers.ModelSerializer):
    pass


class GenresSerializer(serializers.ModelSerializer):
    pass


class ReviewsSerializer(serializers.ModelSerializer):
    pass


class TitleSerializer(serializers.ModelSerializer):
    pass
