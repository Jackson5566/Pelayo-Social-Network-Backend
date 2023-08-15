from django.db.models import Model
from api.classes.controller_logic_excecutor import ResponseBody
from posts_app.classes.posts_classes.bases.post_create_update_operations import PostCreateUpdateOperations
from posts_app.models import PostModel
from rest_framework import status
from typing import Union


class UpdatePost(PostCreateUpdateOperations):

    def __init__(self, request):
        PostCreateUpdateOperations.__init__(self, request=request)

    def get_default_instance(self, model_id=None) -> Union[None, Model]:
        return PostModel.objects.get(id=self.request_manager.request.data.get('id'))

    def create_or_update_process(self):
        if self.is_post_from_authenticated_user(post_instance=self.post_instance_manager.instance):
            self.update_post()
            self.response = ResponseBody(data={'message': 'Éxito con la actualización'}, status=status.HTTP_200_OK)

        else:
            self.response = ResponseBody(data={'message': 'No permitido'}, status=status.HTTP_403_FORBIDDEN)

    def update_post(self):
        files_instances = self.create_files()

        self.post_instance_manager.instance = self.post_serializer_manager.serializer.update(
            validated_data=self.post_serializer_manager.serializer.validated_data,
            instance=self.post_instance_manager.instance)
        self.add_files(files_instances=files_instances)

        self.post_instance_manager.instance.categories.clear()
        self.set_categories()
