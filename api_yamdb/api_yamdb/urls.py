from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf.urls.static import static

from rest_framework import routers

from api.views import (
    # CommentViewSet,
    # FollowViewSet,
    # GroupViewSet,
    # PostViewSet,
    UserViewSet,
    TokenObtainPairView,
    create,
)

router = routers.DefaultRouter()

# router.register(r'posts', PostViewSet)
# router.register(r'^groups', GroupViewSet)
# router.register(r'^groups/(?P<group_id>\d+)', GroupViewSet)
# router.register(r'follow', FollowViewSet, basename='follow')
# router.register(r'^posts/(?P<post_id>\d+)/comments', CommentViewSet)
router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/token/', TokenObtainPairView.as_view()),
    path('api/v1/auth/signup/', create),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]
