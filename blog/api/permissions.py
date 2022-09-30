from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True
            
        return bool(
            request.user.is_authenticated and request.user.is_superuser or
            request.user.is_authenticated and obj.author == request.user
        )



class IsAuthor(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_author or
            request.user and request.user.is_superuser or
            request.user and request.user.is_admin
            )