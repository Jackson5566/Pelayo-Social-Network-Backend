from api.classes.controller_logic_excecutor import ResponseBody
from api.serializers import CommentBaseSerializer
from message_app.serializer import CommentSerializer
from rest_framework import status
from .comment_operations import CommentOperations
from api.decorators.validate_serializer import validate_serializer
from api.classes.type_alias.operations import CreateUpdateOperation
from api.classes.serialzer_operations import SerializerOperations


class CreateUpdateCommentOperations(CommentOperations, CreateUpdateOperation):
    """Al igual que CommentOperations, se encargara de expander una clase, en este caso la anteriormente mencionada
    Al ser las operaciones de acrualizacion y creacion tan similares, se hace necesario una clase para compartir
    funcionalidades"""

    def __init__(self, request, model_id=None):
        CommentOperations.__init__(self, request=request, model_id=model_id)
        SerializerOperations.__init__(self)

    def _get_serializer(self, **kwargs):
        return CommentSerializer(data=self.request_manager.request.data,
                                 context={'request': self.request_manager.request})

    @validate_serializer('serializer_manager')
    def start_process(self) -> None:
        self.create_or_update_process()
        self.set_resulted_message()

    def set_resulted_message(self) -> None:  # Se estará viendo en response
        message_to_return_serializer = CommentBaseSerializer(instance=self.instance_manager.instance)
        self.response = ResponseBody(data=message_to_return_serializer.data, status=status.HTTP_201_CREATED)
