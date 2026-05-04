from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsPrincipal(BasePermission):
    """
    Allows access only to principal users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'principal')

class IsTeacher(BasePermission):
    """
    Allows access only to teacher users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'teacher')

class IsStudent(BasePermission):
    """
    Allows access only to student users.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'student')

class IsPrincipalOrReadOnly(BasePermission):
    """
    Principal has full access, others have read-only.
    Requires authentication for any access.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.role == 'principal'

class IsTeacherOrReadOnly(BasePermission):
    """
    Teachers and Principals have edit access, others read-only.
    Requires authentication for any access.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.method in SAFE_METHODS:
            return True
        return request.user.role in ['principal', 'teacher']

class IsTeacherOrPrincipalReadOnly(BasePermission):
    """
    Teachers and Principals have read access, Principals can edit.
    Custom logic can be added per view.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        if request.user.role in ['principal', 'teacher']:
            return True
        return False

