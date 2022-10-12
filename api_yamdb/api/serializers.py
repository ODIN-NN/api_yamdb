from unicodedata import category
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from datetime import date, datetime
from django.shortcuts import get_object_or_404
from users.models import User
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title
)
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )

    class Meta:
        model = User
        fields = ('username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role')


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        required=True,
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, value):
        username = value['username']
        if username == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено'
            )
        return value


class ObtainTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    # year = serializers.DateField(format="%Y", input_formats=["%Y"])
    rating = serializers.IntegerField(required=False)
    # genre_slug = serializers.SerializerMethodField()
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')

    # def get_genre_slug(self, obj):
    #     print(f'ПЕЧАТАЕМ obj {obj}')
    #     return f'!!!!!{obj}'

class TitleListSerializer(serializers.ModelSerializer):
    # year = serializers.DateField(format="%Y", input_formats=["%Y"])
    rating = serializers.IntegerField(required=False)
    genre = GenreSerializer(many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')

class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
#        queryset=User.objects
    )
    title = SlugRelatedField(
        slug_field='name',
        read_only=True,
#       queryset=Title.objects
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(
                title=title, author=author
            ).exists():
                raise ValidationError(
                    'На произведение возможен только один отзыв.'
                )
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
#        validators = [
#            UniqueValidator(
#                queryset=Review.objects.all(),
#                fields=('title', 'author')
#            )
#        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
        #        queryset=User.objects
    )
    review = SlugRelatedField(
        slug_field='id',
        read_only=True,
        #       queryset=Title.objects
    )
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date', 'review')
