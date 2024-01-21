from rest_framework import status
from api.classes.controller_logic_excecutor import ResponseBody
from posts_app.classes.posts_classes.bases.post_operations import PostOperations
from api.classes.type_alias.operations import DeleteProcessor
from api.decorators.add_security import user_protected


class DeletePost(PostOperations, DeleteProcessor):
    def __init__(self, request, post_id):
        super().__init__(request=request, model_id=post_id)

    def start_process(self):
        @user_protected(
            instance=self.instance_manager.instance.user,
            user=self.request_manager.request.user
        )
        def delete_process():
            self.delete()
            self.response = ResponseBody(data={'message': 'Eliminado con éxito'}, status=status.HTTP_200_OK)

    def delete(self):
        self.instance_manager.instance.files.all().delete()
        self.instance_manager.instance.messages.all().delete()
        self.instance_manager.instance.delete()
