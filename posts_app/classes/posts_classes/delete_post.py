from rest_framework import status
from api.classes.controller_logic_excecutor import ResponseBody
from posts_app.classes.posts_classes.bases.post_operations import PostOperations
from api.classes.type_alias.operations import DeleteProcessor


class DeletePost(PostOperations, DeleteProcessor):
    def __init__(self, request, post_id):
        super().__init__(request=request, model_id=post_id)

    def start_process(self):
        self.delete()
        self.response = ResponseBody(data={'message': 'Deleted'}, status=status.HTTP_200_OK)

    def delete(self):
        self.instance_manager.instance.delete()
