from rest_framework import generics, permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import UsersSerializer
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from .classes.expirationLink import UserExpirationLink
from .classes.denunciate import DenunciateUser


class PasswordChangeRequestView(generics.GenericAPIView, UserExpirationLink):
    def post(self, request):
        self.email = request.data.get('email')
        self.user = User.objects.get(email=self.email)
        self.send_link(template='password_reset_email.html')
        return Response({'message': 'Se ha enviado un email que te permitirá cambiar tu contraseña.'},
                        status=status.HTTP_200_OK)


class PasswordChangeConfirmView(generics.GenericAPIView, UserExpirationLink):
    def post(self, request, token):
        self.set_user(token)
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if password == confirm_password:
            self.user.set_password(password)
            self.user.save()
            return Response({'message': 'Contraseña cambiada correctamente.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Las contraseñas no coinciden.'}, status=status.HTTP_400_BAD_REQUEST)


class CreateUser(generics.GenericAPIView, UserExpirationLink):
    def post(self, request):
        users_serializer = UsersSerializer(data=request.data)

        if users_serializer.is_valid():
            self.email = request.data['email']

            self.user = users_serializer.create(validated_data=users_serializer.data)
            self.user.is_active = False
            self.user.save()

            self.subject = 'Confirmación de cuenta'
            self.send_link(template='user_confirmation_email.html')

            return Response({
                'message': 'Mail de ocnfirmacion enviado'
            }, status=200)

        return Response(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUserConfirmation(generics.GenericAPIView, UserExpirationLink):
    def get(self, request, token):
        self.set_user(token=token)

        self.user.is_active = True
        self.user.save()

        refresh = RefreshToken.for_user(self.user)

        return Response({'refresh': str(refresh), 'access': str(refresh.access_token), },
                        status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def denunciate(request):
    user_reported_id = request.data.get('id')
    denunciation_user = DenunciateUser(user_who_reported=request.user, user_reported_id=user_reported_id)
    return denunciation_user.start_denunciate_proccess()


class UsersView(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]

