from rest_framework.views import APIView
from api.decorators.add_security import access_protected
from .classes.get_user_operation import GetUserOperation
from api.shortcuts.data_get import process_and_get_response
from users_app.classes.update_user_operation import UpdateUser


@access_protected
class SelectUserViewSet(APIView):
    def get(self, request, id):
        get_user_operation = GetUserOperation(request=request, user_id=id)
        return process_and_get_response(get_user_operation)


@access_protected
class CurrentUserInformation(APIView):
    def get(self, request):
        authenticated_user = self.request.user
        get_user_operation = GetUserOperation(request=request, user_instance=authenticated_user)
        return process_and_get_response(get_user_operation)

    def patch(self, request):
        authenticated_user = self.request.user
        update_user = UpdateUser(request=request, user_instance=authenticated_user)
        return process_and_get_response(update_user)



    # user_serializer = UserInformationSerializer(data=request.data,
    #                                             fields=[self.request.query_params.get('changeField')])
    # if user_serializer.is_valid():
    #     user_serializer.update(instance=request.user, validated_data=user_serializer.validated_data)
    #     return Response({
    #         'message': 'Actualizacion con exito'
    #     }, status=status.HTTP_200_OK)
    # return Response(status=status.HTTP_400_BAD_REQUEST)

# @access_protected
# class SelectCurrentlyUserViewSet(APIView):
#     def get(self, request):
#         authenticated_user = self.request.user
#         get_user_operation = GetUserOperation(request=request, user_instance=authenticated_user)
#         return process_and_get_response(get_user_operation)


# unir ambas clases en una
