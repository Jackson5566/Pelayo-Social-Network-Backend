from django.db.models import Model
from api.classes.controller_logic_excecutor import ResponseBody
from .comment_operations import CommentOperations
from ..models import MessagesModel
from message_app.serializer import CommentSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from typing import Union


class GetCommentOperation(CommentOperations):
    def __init__(self, request, post_id):
        super().__init__(request=request, model_id=post_id) # El metodo get_default_instance esta siendo llamado desde
                                                            # Comment Operations, los parametros del mismo deben pasarse
                                                            # por ende en el constructor

    def start_process(self):
        message_data = self.get_message_serializer().data
        self.response = ResponseBody(data=message_data, status=status.HTTP_200_OK)

    def get_default_instance(self, model_id=None) -> Union[None, Model]:
        return get_object_or_404(MessagesModel, id=model_id)

    def get_message_serializer(self):
        return CommentSerializer(self.comment_instance_manager.instance, many=False, fields=['title', 'content'])
