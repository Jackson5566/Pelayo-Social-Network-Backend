from api.decorators.validate_serializer import validate_serializer
from .create_update_comment_operations import CreateUpdateCommentOperations
from ..models import MessagesModel
from typing import Union
from django.db.models import Model


class UpdateCommentOperation(CreateUpdateCommentOperations):
    def __init__(self, request):
        super().__init__(request=request)

    def get_default_instance(self, model_id=None) -> Union[None, Model]:
        return MessagesModel.objects.get(id=self.request_manager.request.data.get('id'))

    @validate_serializer('comment_serializer_manager')
    def create_or_update_process(self):
        self.comment_instance_manager.instance = self.comment_serializer_manager.serializer.update(
            instance=self.comment_instance_manager.instance,
            validated_data=self.comment_serializer_manager.serializer.validated_data)
