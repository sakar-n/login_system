from rest_framework.permissions import BasePermission
from rest_framework import permissions

class MyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return False
    
class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        admin_permission = super().has_permission(request, view)
        return super().has_permission(request, view)
        
       