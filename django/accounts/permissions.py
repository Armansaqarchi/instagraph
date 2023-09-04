from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

    
class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.user.is_authenticated:
            return True if obj.id == request.user.account.id else False
        return False