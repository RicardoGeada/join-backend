from rest_framework.permissions import BasePermission

class IsOwnContactOrNoUserContact(BasePermission):
    """
    Allow user to edit their own contact info and contacts whithout active_user.
    """
    def has_object_permission(self, request, view, obj):
        
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return (obj.active_user == request.user or obj.active_user is None)