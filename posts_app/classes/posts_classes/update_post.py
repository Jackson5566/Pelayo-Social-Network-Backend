from api.classes.controller_logic_excecutor import ResponseBody
from posts_app.classes.posts_classes.bases.post_create_update_operations import PostCreateUpdateOperations
from rest_framework import status


class UpdatePost(PostCreateUpdateOperations):

    def __init__(self, request):
        post_id = request.data.get('id')
        super().__init__(request=request, model_id=post_id)

    def create_or_update_process(self):
        if self.is_post_from_authenticated_user(post_instance=self.model_instance_manager.instance):
            self.update_post()
            self.response = ResponseBody(data={'message': 'Éxito con la actualización'}, status=status.HTTP_200_OK)

        else:
            self.response = ResponseBody(data={'message': 'No permitido'}, status=status.HTTP_403_FORBIDDEN)

    def update_post(self):
        files_instances = self.create_files()

        self.model_instance_manager.instance = self.serializer_manager.serializer_class.update(
            validated_data=self.serializer_manager.serializer.validated_data,
            instance=self.model_instance_manager.instance)
        self.add_files(files_instances=files_instances)

        self.model_instance_manager.instance.categories.clear()
        self.set_categories()
