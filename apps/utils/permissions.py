# encoding: utf-8

"""
# @Time    : 6/2/2020 3:11 下午
# @Author  : Function
# @FileName    : permissions.py
# @Software: PyCharm

权限管理

"""
from rest_framework import permissions
class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`.
        return obj.user == request.user