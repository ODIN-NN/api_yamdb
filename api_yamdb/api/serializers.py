from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from users.models import User
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title
)


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
    # name = serializers.StringRelatedField()
    # slug = SlugRelatedField(
    #     slug_field='slug',
    #     queryset = Category.objects.all()
    #     # queryset=Genre.objects.select_related('categories')
    #     # qs = Album.objects.prefetch_related('tracks')
    # )

    class Meta:
        model = Category
        fields = ('name', 'slug', )



class GenreSerializer(serializers.ModelSerializer):
    # name = serializers.StringRelatedField()
    # slug = serializers.SlugRelatedField(
    #     slug_field='slug',
    #     queryset=Genre.objects.all()
    # )

    class Meta:
        model = Genre
        fields = ('name', 'slug', )
        # read_only_fields = ('slug', )


class TitleSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField()
    year = serializers.IntegerField()
    rating = serializers.IntegerField(read_only=True)
    description = serializers.CharField(required=False)
    # genre = GenreSerializer(many=True, read_only=True)
    # category = CategorySerializer(read_only=True)
    genre = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        queryset=Genre.objects.all(),
        required=False
    )
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all()
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
