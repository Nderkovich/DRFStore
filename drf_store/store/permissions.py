from rest_framework import permissions
from store.models import Order


class UserUpdatePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if view.kwargs['pk'] != request.user.id:
            return False
        return True


class OrderOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Order):
        if obj.user.username != request.user.username:
            return False
        return True


class OrderChangePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Order):
        print(obj.status)
        if obj.status not in ('IN_PROGRESS'):
            return False
        return True
