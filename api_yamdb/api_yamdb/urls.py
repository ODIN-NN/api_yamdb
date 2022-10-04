from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import routers

from api.views import (
#     CommentViewSet,
#     FollowViewSet,
#     GroupViewSet,
#     PostViewSet,
#     UserViewSet
)

router = routers.DefaultRouter()
# router.register(r'posts', PostViewSet)
# router.register(r'^groups', GroupViewSet)
# router.register(r'^groups/(?P<group_id>\d+)', GroupViewSet)
# router.register(r'users', UserViewSet)
# router.register(r'follow', FollowViewSet, basename='follow')
# router.register(r'^posts/(?P<post_id>\d+)/comments', CommentViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
#    path('api/v1/', include(router.urls)),
#    path('auth/', include('djoser.urls')),
#    path('api/v1/', include('djoser.urls.jwt')),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
