from rest_framework.permissions import BasePermission



class isFollowerOrPublicPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if not obj.is_private or obj.follower_list.filter(id = request.user.account.id).exists():
            return True
        
        return False