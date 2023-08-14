from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

class IsFollowerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            account_id = request.user.account.id
            if account_id == obj.id:
                return True
            if obj.following_set.filter(follower = account_id).exists():
                return True
        except AttributeError:
            pass
        raise PermissionDenied()
    
class OwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return True if obj.id == request.user.account.id else False