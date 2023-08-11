from posts_app.classes.posts_classes.bases.post_create_update_operations import PostCreateUpdateOperations
from api.classes.view_logic_executor import ViewLogicExecutor
from posts_app.serializer import PostsCreateSerializer
from rest_framework import status


class CreatePost(PostCreateUpdateOperations):
    def __init__(self, request):
        PostCreateUpdateOperations.__init__(self, request=request)

    def _get_serializer_post(self):
        return PostsCreateSerializer(data=self.request.data, context={'request': self.request})

    def start_process(self):
        if self.post_serializer.is_valid():
            self.create_post()
            self._set_response(data={'message': 'Exito con la creación'}, status=status.HTTP_201_CREATED)

        else:
            self._set_response(data={'message': 'Información no válida'}, status=status.HTTP_400_BAD_REQUEST)

    def create_post(self):
        self.post_instance = self.post_serializer.create(validated_data=self.post_serializer.validated_data)

        files_instances = self.create_files()

        self.add_files(files_instances=files_instances)

        self.set_categories()
