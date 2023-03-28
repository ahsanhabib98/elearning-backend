from rest_framework import permissions

class IsUserOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.is_instructor
            or request.user.is_learner
        ):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.id == obj.id:
            return True
        return False

      
class IsInstructorOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated and (
            request.user.is_superuser or request.user.is_instructor
        ):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser is True or (
            request.user.id == obj.user.id and request.user.is_instructor is True
        ):
            return True
        return False


class IsLearnerOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated and (
            request.user.is_superuser or request.user.is_learner
        ):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser is True or (
            request.user.id == obj.user.id and request.user.is_learner is True
        ):
            return True
        return False