from api.decorators.validate_serializer import validate_serializer
from posts_app.models import PostModel
from .create_update_comment_operations import CreateUpdateCommentOperations
from typing import Union
from django.db.models import Model


class CreateCommentOperation(CreateUpdateCommentOperations):
    def __init__(self, request):
        super().__init__(request=request)
        self._post_instance = self.get_commented_post()

    def get_default_instance(self, model_id=None) -> Union[None, Model]:
        return None

    @validate_serializer('comment_serializer_manager')
    def create_or_update_process(self):
        self.comment_instance_manager.instance = self.comment_serializer_manager.serializer.create(
            validated_data=self.comment_serializer_manager.serializer.validated_data)

        self.add_created_message_to_post()

    def add_created_message_to_post(self):
        self._post_instance.messages.add(self.comment_instance_manager.instance)

    def get_commented_post(self):
        post_id = self.request_manager.request.data.get('id')
        return PostModel.objects.get(id=post_id)
