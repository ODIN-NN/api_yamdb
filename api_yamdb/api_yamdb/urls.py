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
router.register(r'titles', TitleViewSet, basename='titles')
# router.register(r'^titles/(?P<id>\d+)', TitleViewSet)
router.register('users', UserViewSet, basename='users')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<id>\d+)/',
    ReviewViewSet,
    basename='review'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews'
    r'/(?P<review_id>\d+)/comments/(?P<id>\d+)/',
    CommentViewSet,
    basename='comment'
)


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
