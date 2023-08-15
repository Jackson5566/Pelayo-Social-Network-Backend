from abc import ABC, abstractmethod
from api.classes.controller_logic_excecutor import ResponseBody
from api.serializers import CommentBaseSerializer
from message_app.serializer import CommentSerializer
from rest_framework import status
from .comment_operations import CommentOperations
from api.classes.create_update_proccesor import CreateUpdateProcessor
from api.classes.serializer_manager import SerializerManager
from api.decorators.validate_serializer import validate_serializer


class CreateUpdateCommentOperations(CommentOperations, CreateUpdateProcessor, ABC):
    """Al igual que CommentOperations, se encargara de expander una clase, en este caso la anteriormente mencionada
    Al ser las operaciones de acrualizacion y creacion tan similares, se hace necesario una clase para compartir
    funcionalidades"""

    def __init__(self, request):
        super().__init__(request=request)
        comment_serializer = self._get_comment_serializer()
        self.comment_serializer_manager = SerializerManager(serializer=comment_serializer)

    @validate_serializer('comment_serializer_manager')
    def start_process(self) -> None:
        self.create_or_update_process()
        self.set_resulted_message()

    def set_resulted_message(self) -> None:  # Se estará viendo en response
        message_to_return_serializer = CommentBaseSerializer(instance=self.comment_instance_manager.instance)
        self.response = ResponseBody(data=message_to_return_serializer.data, status=status.HTTP_201_CREATED)

    def _get_comment_serializer(self) -> CommentSerializer:
        return CommentSerializer(data=self.request_manager.request.data,
                                 context={'request': self.request_manager.request})

    # ¿ Será necesario pasar el contexto en ambos casos ?