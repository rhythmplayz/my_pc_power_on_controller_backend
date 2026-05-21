from rest_framework.permissions import BasePermission

class IsVerifiedUser(BasePermission):
    """
    Allows access only to authenticated users who have been 
    explicitly marked active (verified) by a Django superuser.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_active