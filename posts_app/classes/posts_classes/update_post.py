from posts_app.classes.posts_classes.bases.post_create_update_operations import PostCreateUpdateOperations
from posts_app.serializer import PostsCreateSerializer
from posts_app.models import PostModel
from rest_framework import status


class UpdatePost(PostCreateUpdateOperations):

    def __init__(self, request):
        PostCreateUpdateOperations.__init__(self, request=request)

    def _get_serializer_post(self):
        return PostsCreateSerializer(data=self.request.data)

    def start_process(self):
        if self.post_serializer.is_valid():
            post = PostModel.objects.get(id=self.request.data['id'])

            if self.is_post_from_authenticated_user(post_instance=post):
                self.update_post()
                self._set_response(data={'message': 'Éxito con la actualización'}, status=status.HTTP_200_OK)

            else:
                self._set_response(data={'message': 'No permitido'}, status=status.HTTP_403_FORBIDDEN)

        else:
            self._set_response(data={'message': 'Información no válida'}, status=status.HTTP_400_BAD_REQUEST)

    def update_post(self):
        files_instances = self.create_files()

        self.post_instance = self.post_serializer.update(validated_data=self.post_serializer.validated_data,
                                                         instance=self.post_instance)
        self.add_files(files_instances=files_instances)

        self.post_instance.categories.clear()
        self.set_categories()



