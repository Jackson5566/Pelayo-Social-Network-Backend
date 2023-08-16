from posts_app.models import PostModel
from api.decorators.validate_serializer import validate_serializer
from .create_update_comment_operations import CreateUpdateCommentOperations


class CreateCommentOperation(CreateUpdateCommentOperations):
    def __init__(self, request):
        super().__init__(request=request)
        self._post_instance = self.get_commented_post()

    @validate_serializer('comment_serializer_manager')
    def create_or_update_process(self):
        self.model_instance_manager.instance = self.comment_serializer_manager.serializer_class.create(
            validated_data=self.comment_serializer_manager.serializer_class.validated_data)

        self.add_created_message_to_post()

    def add_created_message_to_post(self):
        self._post_instance.messages.add(self.model_instance_manager.instance)

    def get_commented_post(self):
        post_id = self.request_manager.request.data.get('id')
        return PostModel.objects.get(id=post_id)
