from rest_framework.views import APIView
from api.decorators.add_security import access_protected
from .classes.get_user_operation import GetUserOperation
from api.shortcuts.data_get import process_and_get_response
from users_app.classes.update_user_operation import UpdateUser


# @access_protected
class SelectedUserInfo(APIView):
    def get(self, request, id):
        get_user_operation = GetUserOperation(request=request, user_id=id)
        return process_and_get_response(get_user_operation)


@access_protected
class CurrentUserInformation(APIView):
    def patch(self, request):
        authenticated_user = self.request.user
        update_user = UpdateUser(request=request, user_instance=authenticated_user)
        return process_and_get_response(update_user)
