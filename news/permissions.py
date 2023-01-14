from rest_framework.permissions import BasePermission, SAFE_METHODS




class IsOwnerPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.methodin in SAFE_METHODS or
            (request.user and
             request.user.is_authenticated and
             request.user.author == obj.author
             )
        )
