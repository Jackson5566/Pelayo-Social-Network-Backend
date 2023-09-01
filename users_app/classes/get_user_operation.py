from api.classes.controller_logic_excecutor import ResponseBody
from .basess.user_operations import UserOperations
from api.classes.serialzer_operations import SerializerOperations
from ..serializer import UsersSerializer
from rest_framework import status


class GetUserOperation(UserOperations, SerializerOperations):

    def __init__(self, request, user_id=None, user_instance=None):
        UserOperations.__init__(self, request=request, model_id=user_id, model_instance=user_instance)
        SerializerOperations.__init__(self)

    def _get_serializer(self, **kwargs):
        # fields = self.get_fields()
        context = {'request': self.request_manager.request}
        return UsersSerializer(instance=self.instance_manager.instance, fields=['username', 'last_name', 'id'],
                               context=context, many=False)

    # def get_fields(self):
    #     match self.only():
    #         case 'posts':
    #             return ['posts']
    #         case 'info_posts':
    #             return ['username', 'last_name', 'posts']
    #         case 'info':
    #             return ['username', 'last_name']
    #         case _:
    #             return ['email', 'username', 'last_name', 'id', 'posts']

    def start_process(self):
        self.response = ResponseBody(data=self.serializer_manager.serializer.data, status=status.HTTP_200_OK)
