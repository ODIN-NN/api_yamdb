from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.relations import SlugRelatedField

from users.models import User

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title # Users
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate(self, data):
        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Username указан неверно!')
        return data


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )
    username = serializers.RegexField(
        regex=r'^[\w.@+-]',
        required=True,
        max_length=150
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'username')

    def validate(self, value):
        username = value['username']
        if username == 'me':
            raise serializers.ValidationError('Недопустимое имя')
        return value


class ObtainTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    def validate(self, attrs):
        user = get_object_or_404(
            get_user_model(), username=attrs.get('username')
        )
        if user.confirmation_code != attrs.get('confirmation_code'):
            raise serializers.ValidationError(
                'Некорректный код подтверждения'
            )
        refresh = RefreshToken.for_user(user)
        data = {'access_token': str(refresh.access_token)}
        return data

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):
    # name = serializers.StringRelatedField()
    # slug = SlugRelatedField(
    #     slug_field='slug',
    #     queryset = Category.objects.all()
    #     # queryset=Genre.objects.select_related('categories')
    #     # qs = Album.objects.prefetch_related('tracks')
    # )

    class Meta:
        model = Category
        fields = ('name', 'slug')


class CommentSerializer(serializers.ModelSerializer):
    pass


class GenreSerializer(serializers.ModelSerializer):
    # name = serializers.StringRelatedField()
    # slug = SlugRelatedField(
    #     slug_field='slug',
    #     queryset=Genre.objects.all()
    # )

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):
    pass


class TitleSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()
    year = serializers.IntegerField()
    rating = serializers.IntegerField(read_only=True)
    description = serializers.CharField(required=False)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    # genre = serializers.SlugRelatedField(
    #     slug_field='name',
    #     many=True,
    #     queryset=Genre.objects.all()
    # )
    # category = serializers.SlugRelatedField(
    #     slug_field='name',
    #     queryset=Category.objects.all()
    # )

    class Meta:
        model = Title
        # fields = '__all__'
        fields = ('name', 'year', 'rating', 'description', 'genre', 'category')
