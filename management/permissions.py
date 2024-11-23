from rest_framework.permissions import BasePermission

class IsAdminRole(BasePermission):
    """
    Allows access only to users with the 'admin' role.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
    
class IsMemberRole(BasePermission):
    """
    Allows access only to users with the 'member' role.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'member'
    
class IsAdminOrMember(BasePermission):
    """
    Allow both Admin and Member roles to access the view.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and has an appropriate role
        return request.user.is_authenticated and request.user.role in ['admin', 'member']
