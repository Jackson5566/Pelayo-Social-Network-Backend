from rest_framework import status
from api.classes.controller_logic_excecutor import ResponseBody
from posts_app.classes.posts_classes.bases.post_create_update_operations import PostCreateUpdateOperations


class CreatePost(PostCreateUpdateOperations):
    def __init__(self, request):
        super().__init__(request=request)

    def create_or_update_process(self):
        self.create_post()
        self.response = ResponseBody(data={'message': 'Exito con la creación'}, status=status.HTTP_201_CREATED)

    def create_post(self):
        self.model_instance_manager.instance = self.serializer_manager.serializer_class.create(
            validated_data=self.serializer_manager.serializer_class.validated_data)

        files_instances = self.create_files()

        self.add_files(files_instances=files_instances)

        self.set_categories()
