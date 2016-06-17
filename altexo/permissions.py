from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminUserOrReadOnly(BasePermission):
    """
    The request is authenticated as an admin user, or is a read-only request.
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated():
            return (
                request.method in SAFE_METHODS or
                request.user.is_staff
            )

