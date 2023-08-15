from django.db.models import Model

from api.classes.controller_logic_excecutor import ResponseBody
from posts_app.classes.posts_classes.bases.post_create_update_operations import PostCreateUpdateOperations
from rest_framework import status
from typing import Union


class CreatePost(PostCreateUpdateOperations):
    def __init__(self, request):
        super().__init__(request=request)

    def get_default_instance(self, model_id=None) -> Union[None, Model]:
        return None

    def create_or_update_process(self):
        self.create_post()
        self.response = ResponseBody(data={'message': 'Exito con la creación'}, status=status.HTTP_201_CREATED)

    def create_post(self):
        self.post_instance_manager.instance = self.post_serializer_manager.serializer.create(
            validated_data=self.post_serializer_manager.serializer.validated_data)

        files_instances = self.create_files()

        self.add_files(files_instances=files_instances)

        self.set_categories()
