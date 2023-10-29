from rest_framework import status
from api.classes.controller_logic_excecutor import ResponseBody
from .comment_operations import CommentOperations
from api.classes.type_alias.operations import DeleteProcessor


class DeleteCommentOperation(CommentOperations, DeleteProcessor):
    def __init__(self, request, model_id):
        CommentOperations.__init__(self, request=request, model_id=model_id)
        DeleteProcessor.__init__(self)

    def start_process(self):
        self.delete()
        self.response = ResponseBody(data={'message': 'Deleted'}, status=status.HTTP_200_OK)

    def delete(self):
        if self.instance_manager.instance.user == self.request_manager.request.user:
            self.instance_manager.instance.delete()
