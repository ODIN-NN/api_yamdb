import secrets
import io
from rest_framework.parsers import JSONParser
from django.forms.models import model_to_dict
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, serializers, mixins, permissions, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Avg
from django.http import Http404
from api_yamdb.settings import FROM_EMAIL
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title
)
from users.models import User
from .permissions import IsAdmin, IsAdminModeratorAuthorOrReadOnly
from .serializers import (
    CommentSerializer,
    CategorySerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
    TitleListSerializer,
    UserSerializer,
    SignUpSerializer,
    ObtainTokenSerializer,
)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create(request):
    """Отправка кода подтверждения при регистрации."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    secret_code = secrets.token_urlsafe()
    user, _ = User.objects.get_or_create(
        username=serializer.data['username'],
        email=serializer.data['email'],
        confirmation_code=secret_code
    )
    message = ('Для завершения регистрации на сайте введите '
               f'confirmation_code: {secret_code}')
    send_mail(
        subject='Registration',
        message=message,
        from_email=FROM_EMAIL,
        recipient_list=[user.email]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def get_token(request):
    """Отправка токена для завершения регистрации."""
    serializer = ObtainTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user = User.objects.get(username=serializer.validated_data['username'])
    except User.DoesNotExist:
        return Response(
            'Пользователь не найден', status=status.HTTP_404_NOT_FOUND
        )
    if (user.confirmation_code != serializer.validated_data[
            'confirmation_code']):
        return Response(
            'Неверный код подтверждения', status=status.HTTP_400_BAD_REQUEST
        )
    refresh = RefreshToken.for_user(user)
    return Response(
        {'token': str(refresh.access_token)}, status=status.HTTP_200_OK
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=(permissions.IsAuthenticated,),
        url_path='me',
    )
    def my_profile(self, request, *args, **kwargs):
        """Запросы для получения и изменения данных."""
        if request.method == 'PATCH':
            serializer = self.get_serializer(self.request.user,
                                             data=request.data,
                                             partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, slug=lookup_field):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, slug=lookup_field):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def retrieve(self, request, slug=lookup_field):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, slug=lookup_field):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    # serializer_class = TitleSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('genre', 'category')
    # genre_slug = TitleSerializer(queryset)
    # data = list(Genre.objects.all().values('slug'))
    # genre_slug = list((obj['slug'] for obj in data))
    # print(f'ПЕЧАТАЕМ genre_slug {genre_slug}')
    # print(f'ПЕЧАТАЕМ genre_slug {dir(genre_slug)}')
    # search_fields = ('category', 'genre', 'name', 'year', 'genre_slug')
    lookup_field = 'id'

    # def get_queryset(self):
    #     genre_slug = self.request.query_params.get('genre')
    #     print(f'ПЕЧАТАЕМ genre_slug {genre_slug}')
    #     if genre_slug is not None:
    #         genre_slug_id = Genre.objects.get(slug=genre_slug)
    #         print(f'ПЕЧАТАЕМ genre_slug_id {genre_slug_id}')
    #         queryset = Title.objects.filter(genre=genre_slug_id)
    #         print(f'ПЕЧАТАЕМ genre_slug_id_queryset {queryset}')
    #     else:
    #         queryset = Title.objects.all()
    #     return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return TitleListSerializer
        return TitleSerializer

    def get_permissions(self):
        if self.action == 'list' or self.request.auth == None:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
        else:
            permission_classes = [IsAdmin]
        return [permission() for permission in permission_classes]

    def retrieve(self, request, id=lookup_field):
        queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
        title = get_object_or_404(queryset, pk=id)
        serializer_class = TitleListSerializer(title)
        return Response(serializer_class.data)


class ReviewViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = ReviewSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly)
    pagination_class = LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())




class CommentViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    serializer_class = CommentSerializer
    permission_classes = (IsAdminModeratorAuthorOrReadOnly,
                          permissions.IsAuthenticatedOrReadOnly)
    pagination_class = LimitOffsetPagination

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
