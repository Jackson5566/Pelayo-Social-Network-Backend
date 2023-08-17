from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions


def access_protected(cls):
    setattr(cls, 'permission_classes', [permissions.IsAuthenticated])
    setattr(cls, 'authentication_classes', [JWTAuthentication])
    return cls
