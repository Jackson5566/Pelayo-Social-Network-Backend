from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions


def access_protected(cls):
    setattr(cls, 'permission_classes', [permissions.IsAuthenticated])
    setattr(cls, 'authentication_classes', [JWTAuthentication])
    return cls


def user_protected(instance, user):
    def look(func):

        if instance == user:
            func()

        else:
            # Tal vez definir algún tipo de mecanismo, porque significa un problema de seguridad
            raise Exception("No tienes autorizacion")

    return look
