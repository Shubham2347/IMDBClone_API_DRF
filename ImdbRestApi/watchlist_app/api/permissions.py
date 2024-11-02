from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS
#custom permission
class AdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return bool(request.user and request.user.is_staff)

class ReviewUserOrReadOnly(permissions.BasePermission):
     
     def has_permission(self, request, view, obj):
         if request.method in permissions.SAFE_METHODS:
             return True
         else:
             return obj.review_user == request.user

    