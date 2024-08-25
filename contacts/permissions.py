from rest_framework.permissions import BasePermission

class IsOwnContactOrNoUserContact(BasePermission):
    """
    Custom permission to allow users to edit their own contact information or 
    contacts that do not have an associated active user.

    Permissions:
        - Any user can perform safe methods (GET, HEAD, OPTIONS).
        - Only the user associated with the contact (`active_user`) or if the 
          contact has no associated active user (`active_user` is None) can edit the contact.
    """
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to interact with the given contact object.

        Args:
            request: The HTTP request being processed.
            view: The view handling the request.
            obj: The contact object being accessed.

        Returns:
            bool: True if the request method is safe (GET, HEAD, OPTIONS),
                  or if the user is the `active_user` of the contact,
                  or if the contact has no `active_user`. Otherwise, False.
        """
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return (obj.active_user == request.user or obj.active_user is None)