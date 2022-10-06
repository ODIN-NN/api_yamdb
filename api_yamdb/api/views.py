import secrets

from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions, viewsets, filters, status
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt import tokens
from rest_framework_simplejwt.views import TokenViewBase

from reviews.models import Categories, Comments, Genres, Reviews, Title
from users.models import User
from .permissions import IsAdmin
from .serializers import (
    CommentsSerializer,
    CategoriesSerializer,
    GenresSerializer,
    ReviewsSerializer,
    TitleSerializer,
    UserSerializer,
    SignUpSerializer,
    ObtainTokenSerializer,
)
from api_yamdb.settings import DEFAULT_FROM_EMAIL, HOST_NAME


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def create(request):
    """Отправка кода подтверждения при регистрации."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    token = secrets.token_urlsafe()
    user, _ = get_user_model().objects.get_or_create(
        username=serializer.data.get('username'),
        email=serializer.data.get('email'),
        confirmation_code=token
    )
    message = ('Для завершения регистрации на сайте введите'
               f'confirmation_code={token}')
    send_mail(
        subject='Регистрация на сайте',
        message=message,
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[user.email]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


# class CustomAuthToken(CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (permissions.AllowAny,)
#     serializer_class = ObtainTokenSerializer

#     def get_token(self, request):
#         """Отправка token."""
#         serializer = ObtainTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         username = serializer.data.get('username')
#         confirmation_code = serializer.data.get('confirmation_code')
#         user = get_object_or_404(User, username=username)
#         if default_token_generator.check_token(user, confirmation_code):
#             token = tokens.AccessToken.for_user(user)
#             return Response({'token': f'{token}'}, status=status.HTTP_200_OK)
#         return Response({'confirmation_code': 'Неверный код подтверждения'},
#                         status=status.HTTP_400_BAD_REQUEST)

class TokenObtainPairView(TokenViewBase):
    serializer_class = ObtainTokenSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['GET', 'PATCH'],
        permission_classes=(permissions.IsAuthenticated,),
        url_path='me',
    )
    def my_profile(self, request):
        """Запросы на для получения и изменения данных пользователей."""
        if request.method == 'PATCH':
            serializer = UserSerializer(self.request.user,
                                        data=request.data,
                                        partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


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
