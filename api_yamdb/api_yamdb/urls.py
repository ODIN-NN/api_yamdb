from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from rest_framework import routers

from api.views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UserViewSet,
    get_token,
    create,
    ReviewViewSet,
    CommentViewSet,
)

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
# router.register(r'categories/(?P<slug>[a-z0-9]+)', CategoryViewSet, basename='category-slug')
router.register(r'genres', GenreViewSet)
router.register(r'titles', TitleViewSet)
# router.register(r'^titles/(?P<id>\d+)', TitleViewSet)
router.register('users', UserViewSet, basename='users')
#router.register(r'reviews', ReviewViewSet, basename='rewiews')
#router.register(r'^reviews/(?P<reviews_id>\d+)', ReviewViewSet)
#router.register('comments', CommentViewSet, basename='comments')
#router.register(r'^comments/(?P<comments_id>\d+)', CommentViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/token/', get_token),
    path('api/v1/auth/signup/', create),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
