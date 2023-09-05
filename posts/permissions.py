from rest_framework.permissions import BasePermission



class IsFollowerOrPublicPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user.account or \
        not obj.is_private or \
        obj.followers_list.filter(id = request.user.account.id).exists():
            return True
        
        return False