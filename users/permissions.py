from rest_framework import permissions

class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'super_admin'

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'admin'

class IsUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'user'