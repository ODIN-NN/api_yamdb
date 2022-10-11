from rest_framework import permissions
from users.models import User


class IsAdmin(permissions.BasePermission):
    message = 'Доступ только для админов и суперпользователей'

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser
        )


class IsAdminModeratorAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == User.admin
                or request.user.role == User.moderator
                or obj.author == request.user)
