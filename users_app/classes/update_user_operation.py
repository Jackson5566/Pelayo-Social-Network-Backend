from rest_framework import status
from .basess.user_operations import UserOperations
from api.classes.serialzer_operations import SerializerOperations
from ..serializer import UsersSerializerReturn2
from api.decorators.validate_serializer import validate_serializer
from api.classes.controller_logic_excecutor import ResponseBody


class UpdateUser(UserOperations, SerializerOperations):
    def __init__(self, request, user_id=None, user_instance=None):
        UserOperations.__init__(self, request=request, model_id=user_id, model_instance=user_instance)
        SerializerOperations.__init__(self)

    def _get_serializer(self, **kwargs):
        field = self.request_manager.request.query_params.get('changeField')
        return UsersSerializerReturn2(data=self.request_manager.request.data,
                               fields=[field])

    @validate_serializer('serializer_manager')
    def start_process(self):
        self.serializer_manager.serializer.update(instance=self.instance_manager.instance,
                                                  validated_data=self.serializer_manager.serializer.validated_data)
        self.response = ResponseBody(data={
            'message': 'Actualizacion con exito'
        }, status=status.HTTP_200_OK)
