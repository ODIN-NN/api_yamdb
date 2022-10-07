import secrets

from django.core.mail import send_mail
from rest_framework import viewsets, permissions, viewsets, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api_yamdb.settings import FROM_EMAIL
from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title
)
from users.models import User
from .permissions import IsAdmin
from .serializers import (
    CommentSerializer,
    CategorySerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleSerializer,
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
    # permission_classes = (IsAdmin, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    pagination_class = LimitOffsetPagination


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    # permission_classes = (IsAdmin, )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category', 'genre', 'name', 'year')

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_review(self):
        return get_object_or_404(Review, pk=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
