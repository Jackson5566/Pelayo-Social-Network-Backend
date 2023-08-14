from abc import ABC
from .create_update_comment_operations import CreateUpdateCommentOperations
from ..models import MessagesModel


class UpdateCommentOperation(CreateUpdateCommentOperations, ABC):
    def __init__(self, request):
        super().__init__(request=request)

    def get_default_message_instance(self):
        return MessagesModel.objects.get(id=self.request_manager.request.data.get('id'))

    def create_or_update_process(self):
        self.message_instance = self.comment_serializer.update(instance=self.message_instance,
                                                               validated_data=self.comment_serializer.validated_data)