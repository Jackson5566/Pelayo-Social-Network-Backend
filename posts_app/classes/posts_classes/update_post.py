from .post_base import PostCreateUpdateBase, PostBase
from posts_app.serializer import PostsCreateSerializer
from posts_app.models import PostModel
from .post_processor import PostCreateUpdateProcessor
from rest_framework import status


class UpdatePost(PostCreateUpdateBase, PostBase):

    def __init__(self, request):
        PostBase.__init__(self, request=request)
        PostCreateUpdateBase.__init__(self)
        self.post_instance = None

    def _get_serializer_post(self):
        return PostsCreateSerializer(data=self.request.data)

    def start_update_post(self):
        files_instances = PostCreateUpdateProcessor.serialize_files(request=self.request)

        if self.post_serializer.is_valid():
            post = PostModel.objects.get(id=self.request.data['id'])

            post.categories.clear()
            PostCreateUpdateProcessor.set_categories(request=self.request, post_instance=post)

            if self.request.user == post.user:
                post_instance = self.post_serializer.update(validated_data=self.post_serializer.validated_data,
                                                            instance=post)
                PostCreateUpdateProcessor.add_files(post_instance=post_instance, files_instances=files_instances)
                self._set_response(data={'message': 'Éxito con la actualización'}, status=status.HTTP_200_OK)

            else:
                self._set_response(data={'message': 'No permitido'}, status=status.HTTP_403_FORBIDDEN)

        else:
            self._set_response(data={'message': 'Información no válida'}, status=status.HTTP_400_BAD_REQUEST)