from rest_framework import status
from api.classes.controller_logic_excecutor import ResponseBody
from api.decorators.add_security import user_protected
from .comment_operations import CommentOperations
from api.classes.type_alias.operations import DeleteProcessor


class DeleteCommentOperation(CommentOperations, DeleteProcessor):
    def __init__(self, request, model_id):
        CommentOperations.__init__(self, request=request, model_id=model_id)
        DeleteProcessor.__init__(self)

    def start_process(self):
        @user_protected(
            instance=self.instance_manager.instance.user,
            user=self.request_manager.request.user
        )
        def delete_process():
            self.delete()
            self.response = ResponseBody(data={'message': 'Deleted'}, status=status.HTTP_200_OK)

    def delete(self):
        self.instance_manager.instance.delete()
