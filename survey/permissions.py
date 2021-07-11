from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class CreationOnlyAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return True if request.user.is_staff or request.method in SAFE_METHODS else False


class IsAuthorAccess(permissions.BasePermission):

    def has_permission(self, request, view):
        return int(request.path.split('/')[-2]) == request.user.pk
