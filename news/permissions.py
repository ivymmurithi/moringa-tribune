from rest_framework.permissions import SAFE_METHODS, BasePermission

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # SAFE_METHODS are request methods that do not change the database like the GET method
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_staff