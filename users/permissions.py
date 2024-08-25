from rest_framework.permissions import BasePermission

class IsSelfOrReadOnly(BasePermission):
    """
    Custom permission to allow users to edit their own data and read the data of other users.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the request has permission to access the object.
        
        Returns:
            bool: True if the request method is read-only (GET, HEAD, OPTIONS) or if the user is the owner of the object; otherwise False.
        """
        # allways allow read request
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        # only allow edit requests for own user
        return obj == request.user