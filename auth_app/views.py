from rest_framework.views import APIView
from .models import User
from .serializer import UsersSerializer
from rest_framework.response import Response
from .classes.denunciate import DenunciateUser
from rest_framework_simplejwt.tokens import RefreshToken
from api.shortcuts.data_get import process_and_get_response
from rest_framework import generics, permissions, viewsets, status
from .classes.expirationLink import GetUserFromExpirationLink, SendUserExpirationLink
from api.decorators.add_security import access_protected
from django.shortcuts import get_object_or_404


# Simplificar más este código

class PasswordChangeRequestView(generics.GenericAPIView):
    def post(self, request):
        send_user_expiration_link = SendUserExpirationLink()
        send_user_expiration_link.utilities.user_email = request.data.get('email')

        send_user_expiration_link.utilities.user = get_object_or_404(
            User, email=send_user_expiration_link.utilities.user_email)

        send_user_expiration_link.send_link(template='password_reset_email.html', subject="Password Reset Link")
        return Response({'message': 'Se ha enviado un email que te permitirá cambiar tu contraseña.'},
                        status=status.HTTP_200_OK)


class PasswordChangeConfirmView(generics.GenericAPIView):
    def post(self, request, token):
        get_user_from_expiration_link = GetUserFromExpirationLink()
        get_user_from_expiration_link.set_user(token)

        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if password == confirm_password:
            get_user_from_expiration_link.utilities.user.set_password(password)
            get_user_from_expiration_link.utilities.user.save()
            return Response({'message': 'Contraseña cambiada correctamente.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Las contraseñas no coinciden.'}, status=status.HTTP_400_BAD_REQUEST)


class CreateUser(generics.GenericAPIView):
    def post(self, request):
        send_user_expiration_link = SendUserExpirationLink()
        users_serializer = UsersSerializer(data=request.data)

        if users_serializer.is_valid():
            send_user_expiration_link.utilities.email = request.data['email']

            send_user_expiration_link.utilities.user = users_serializer.create(validated_data=users_serializer.data)
            send_user_expiration_link.utilities.user.is_active = False
            send_user_expiration_link.utilities.user.save()

            send_user_expiration_link.send_link(template='user_confirmation_email.html',
                                                subject='Confirmación de cuenta')

            return Response({
                'message': 'Mail de confirmación enviado'
            }, status=200)

        return Response(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUserConfirmation(generics.GenericAPIView):
    def get(self, request, token):
        get_user_from_expiration_link = GetUserFromExpirationLink()
        get_user_from_expiration_link.set_user(token=token)

        get_user_from_expiration_link.utilities.user.is_active = True
        get_user_from_expiration_link.utilities.user.save()

        refresh = RefreshToken.for_user(get_user_from_expiration_link.utilities.user)

        return Response({'refresh': str(refresh), 'access': str(refresh.access_token), },
                        status=status.HTTP_201_CREATED)


@access_protected
class Complaint(APIView):
    def post(self, request):
        denunciation_user = DenunciateUser(request=request)
        return process_and_get_response(denunciation_user)


class UsersView(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
