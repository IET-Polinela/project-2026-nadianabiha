from rest_framework import permissions


class IsCitizen(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and getattr(request.user, 'is_member', False)
            and not getattr(request.user, 'is_admin', False)
        )


class IsOwnerAndDraftOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated
            and obj.reporter == request.user
            and obj.status == 'DRAFT'
        )
