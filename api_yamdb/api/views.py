from rest_framework import viewsets, permissions, mixins, viewsets, filters
from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Categories, Comments, Genres, Reviews, Title, # Users
# from .permissions import AuthorOrIsAuth # Настя это тебе
from .serializers import (
    CommentsSerializer,
    CategoriesSerializer,
    GenresSerializer,
    ReviewsSerializer,
    TitleSerializer,
    # UsersSerializer
)

# class UsersViewSet(viewsets.ModelViewSet):
#     pass


class CommentViewSet(viewsets.ModelViewSet):
    pass


class CategoriesViewSet(viewsets.ModelViewSet):
    pass


class GenresViewSet(viewsets.ModelViewSet):
    pass


class GenresViewSet(viewsets.ModelViewSet):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    pass
