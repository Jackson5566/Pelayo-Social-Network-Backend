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
from users_app.serializer import UsersSerializerReturn2
from django.core.mail import send_mail
from django.template.loader import render_to_string
from threading import Thread

# Simplificar más este código

class PasswordChangeRequestView(generics.GenericAPIView):
    send_user_expiration_link = SendUserExpirationLink()

    def post(self, request):
        user_email = request.data.get('email')

        self.send_user_expiration_link.utilities.user = get_object_or_404(
            User, email=user_email)

        self.send_user_expiration_link.send_link(template='password_reset_email.html', subject="Password Reset Link")
        return Response({'message': 'Se ha enviado un email que te permitirá cambiar tu contraseña.'},
                        status=status.HTTP_200_OK)


class PasswordChangeConfirmView(generics.GenericAPIView):
    get_user_from_expiration_link = GetUserFromExpirationLink()

    def post(self, request, token):
        self.get_user_from_expiration_link.set_user(token)

        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if password == confirm_password:
            self.get_user_from_expiration_link.utilities.user.set_password(password)
            self.get_user_from_expiration_link.utilities.user.save()
            return Response({'message': 'Contraseña cambiada correctamente.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Las contraseñas no coinciden.'}, status=status.HTTP_400_BAD_REQUEST)


class CreateUser(generics.GenericAPIView):
    send_user_expiration_link = SendUserExpirationLink()

    def post(self, request):
        users_serializer = UsersSerializer(data=request.data)

        ancient_user = User.objects.filter(username=request.data.get('username'),
            email=request.data.get('email')).first()
        if ancient_user and not ancient_user.is_active:
            self.send_user_expiration_link.utilities.user = ancient_user

            return self.send_confirmation_email()

        else:
            if users_serializer.is_valid():

                self.send_user_expiration_link.utilities.user = users_serializer.create(validated_data=users_serializer.data)
                self.send_user_expiration_link.utilities.user.is_active = False
                self.send_user_expiration_link.utilities.user.save()

                return self.send_confirmation_email()

            return Response(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def send_confirmation_email(self):
        self.send_user_expiration_link.send_link(template='user_confirmation_email.html',
                                            subject='Confirmación de cuenta')

        return Response({
            'message': 'Mail de confirmación enviado'
        }, status=200)


class CreateUserConfirmation(generics.GenericAPIView):
    get_user_from_expiration_link = GetUserFromExpirationLink()

    def get(self, request, token):
        self.get_user_from_expiration_link.set_user(token=token)

        self.get_user_from_expiration_link.utilities.user.is_active = True
        self.get_user_from_expiration_link.utilities.user.save()

        email_thread = Thread(target=self.send_welcome_email)
        email_thread.start()

        refresh = RefreshToken.for_user(self.get_user_from_expiration_link.utilities.user)

        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)},
                        status=status.HTTP_201_CREATED)

    def send_welcome_email(self):
        message = render_to_string('welcome.html')
        send_mail("Bienvenida", "", None,
          [self.get_user_from_expiration_link.utilities.user.email],
          fail_silently=False, html_message=message)


@access_protected
class Complaint(APIView):
    def post(self, request):
        denunciation_user = DenunciateUser(request=request)
        return process_and_get_response(denunciation_user)

@access_protected
class GetAuthenticatedUser(APIView):
    def get(self, request):
        authenticated_user = request.user
        user_authenticated_serializer = UsersSerializerReturn2(instance=authenticated_user)
        return Response(user_authenticated_serializer.data)


class UsersView(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]

