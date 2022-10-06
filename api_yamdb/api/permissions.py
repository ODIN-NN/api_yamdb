from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    message = 'Доступ только для админов и суперпользователей'

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == 'admin' or request.user.is_superuser
        )
