from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):


    """
    Custom permission to only allow owners of a resource object to edit it.
    Accessible to Admin users.
    """
    def has_object_permission(self, request, view, obj):
        # Allow read-only access for all users.
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow full access to admin users.
        if request.user.is_staff:
            return True
        
        # Check if the object has a 'user' attribute and if the request user is the owner.
        if hasattr(obj, "user") and obj.user == request.user:
            return True
        
        # Check if the object has an 'owner' attribute and if the request user is the owner.
        if hasattr(obj, "owner") and obj.owner == request.user:
            return True
        
        # Check if the object has an 'uploader' attribute and if the request user is the uploader.
        if hasattr(obj, "uploader") and obj.uploader == request.user:
            return True
        
        # Check if the object has a 'created_by' attribute and if the request user is the creator.
        if hasattr(obj, "created_by") and obj.created_by == request.user:
            return True

        
        return False
    


class IsReviewCreatorOrReadOnly(permissions.BasePermission):
     
    """
    Custom permission to only allow owners of a resource object to edit it.
    Accessible to Admin users.
    """
    def has_object_permission(self, request, view, obj):
        # Allow Read-Only access to all users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow full access to admin users.
        if request.user.is_staff:
            return True
        
        # Check if the object has a 'instructor' attribute, then return the truthiness.
        if hasattr(obj, "user"):
            return obj.user == request.user  #review.user = request.user
        
        
        
        