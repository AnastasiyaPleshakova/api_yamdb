from rest_framework import permissions


class IsAnonym(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'POST':
            return True
