from rest_framework import permissions


class UserUpdatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.kwargs['pk'] != request.user.id:
            return False
        return True
