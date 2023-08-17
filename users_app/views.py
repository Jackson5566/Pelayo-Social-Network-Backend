from auth_app.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, generics, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import UsersSerializerReturn, UserInformationSerializer
from api.decorators.add_security import access_protected
from .classes.get_user_operation import GetUserOperation
from api.shortcuts.data_get import process_and_get_response


@access_protected
class SelectUserViewSet(APIView):
    def get(self, request, id):
        get_user_operation = GetUserOperation(request=request, user_id=id)
        return process_and_get_response(get_user_operation)


@access_protected
class SelectCurrentlyUserViewSet(APIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializerReturn
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        authenticated_user = self.request.user
        get_user_operation = GetUserOperation(request=request, user_instance=authenticated_user)
        return process_and_get_response(get_user_operation)


class CurrentUserInformation(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = self.request.user
        user_serializer = UserInformationSerializer(user, many=False)
        return Response(user_serializer.data)

    def patch(self, request):
        user_serializer = UserInformationSerializer(data=request.data,
                                                    fields=[self.request.query_params.get('changeField')])
        if user_serializer.is_valid():
            user_serializer.update(instance=request.user, validated_data=user_serializer.validated_data)
            return Response({
                'message': 'Actualizacion con exito'
            }, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
