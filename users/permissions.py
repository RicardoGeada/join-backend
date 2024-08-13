from rest_framework.permissions import BasePermission

class IsSelfOrReadOnly(BasePermission):
    """
    Allow Users to edit their own data and read the data of other users.
    """
    def has_object_permission(self, request, view, obj):
        # allways allow read request
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        # only allow edit requests for own user
        return obj == request.user