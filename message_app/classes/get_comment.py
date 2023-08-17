from api.classes.controller_logic_excecutor import ResponseBody
from .comment_operations import CommentOperations
from message_app.serializer import CommentSerializer
from rest_framework import status
from api.classes.serialzer_operations import SerializerOperations


class GetCommentOperation(CommentOperations, SerializerOperations):
    def __init__(self, request, post_id):
        CommentOperations.__init__(self, request=request, model_id=post_id)
        SerializerOperations.__init__(self)

    def _get_serializer(self):
        return CommentSerializer(self.instance_manager.instance, many=False, fields=['title', 'content'])

    def start_process(self):
        message_data = self.serializer_manager.serializer.data
        self.response = ResponseBody(data=message_data, status=status.HTTP_200_OK)
