from rest_framework import permissions


class IsAnonymOrCanCorrect(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        role = ['admin', 'moderator']
        return (
            request.method in permissions.SAFE_METHODS
            or request.user == obj.author or (
            (request.user.is_authenticated or request.user.is_superuser)
            and (request.user.role in role))
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            (request.user.is_authenticated or request.user.is_superuser)
            and request.user.role == 'admin')


class IsAllowAny(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return True
