from rest_framework import permissions

class IsCitizen(permissions.BasePermission):
    def has_permission(self, request, view):
        # Citizen didefinisikan sebagai user yang login dan bukan staff/admin
        return request.user.is_authenticated and not request.user.is_staff

class IsOwnerAndDraftOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Akses baca (GET, HEAD, OPTIONS) diizinkan untuk semua user terautentikasi
        if request.method in permissions.SAFE_METHODS:
            return True
            
        return obj.reporter == request.user and obj.status == 'DRAFT'