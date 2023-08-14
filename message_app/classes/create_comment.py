from posts_app.models import PostModel
from .create_update_comment_operations import CreateUpdateCommentOperations


class CreateCommentOperation(CreateUpdateCommentOperations):
    def __init__(self, request):
        super().__init__(request=request)
        self._post_instance = self.get_commented_post()

    def get_default_message_instance(self):
        return None

    def create_or_update_process(self):
        self.message_instance = self.comment_serializer.create(validated_data=self.comment_serializer.validated_data,
                                                               user=self.request_manager.user)
        self.add_created_message_to_post()

    def add_created_message_to_post(self):
        self._post_instance.add(self.message_instance)

    def get_commented_post(self):
        post_id = self.request_manager.data('id')
        return PostModel.objects.get(id=post_id)
