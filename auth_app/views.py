from .models import User
from .serializer import UsersSerializer
from rest_framework.response import Response
from .classes.denunciate import DenunciateUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, permissions, viewsets, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .classes.expirationLink import GetUserFromExpirationLink, SendUserExpirationLink
from rest_framework.decorators import api_view, permission_classes, authentication_classes


class PasswordChangeRequestView(generics.GenericAPIView):
    def post(self, request):
        send_user_expiration_link = SendUserExpirationLink()
        send_user_expiration_link.utilities.user_email = request.data.get('email')
        send_user_expiration_link.utilities.user = User.objects.get(
            email=send_user_expiration_link.utilities.user_email)
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
                'message': 'Mail de ocnfirmacion enviado'
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


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def denunciate(request):
    denunciation_user = DenunciateUser(request=request)
    denunciation_user.start_process()
    return denunciation_user.response


class UsersView(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
