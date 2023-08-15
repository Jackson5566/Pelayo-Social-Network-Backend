from rest_framework import status
from api.classes.controller_logic_excecutor import ResponseBody
from posts_app.classes.posts_classes.bases.post_operations import PostOperations
from typing import Union
from django.db.models import Model
from django.shortcuts import get_object_or_404
from posts_app.models import PostModel


class DeletePost(PostOperations):
    def __init__(self, request, post_id):
        super().__init__(request=request, model_id=post_id)

    def get_default_instance(self, model_id=None) -> Union[None, Model]:
        return get_object_or_404(PostModel, id=model_id)

    def start_process(self):
        self.delete_post()
        self.response = ResponseBody(data={'message': 'Deleted'}, status=status.HTTP_200_OK)

    def delete_post(self):
        self.post_instance_manager.instance.delete()
