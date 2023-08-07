from posts_app.classes.posts_classes.post_processor import PostCreateUpdateProcessor
from .post_base import PostCreateUpdateBase, PostBase
from posts_app.serializer import PostsCreateSerializer
from rest_framework import status


class CreatePost(PostCreateUpdateBase, PostBase):
    def __init__(self, request):
        super().__init__(request=request)

    def _get_serializer_post(self):
        return PostsCreateSerializer(data=self.request.data, context={'request': self.request})

    def create_post(self):
        files_instances = PostCreateUpdateProcessor.serialize_files(self.request)
        if self.post_serializer.is_valid():
            post_instance = self.post_serializer.create(validated_data=self.post_serializer.validated_data)

            PostCreateUpdateProcessor.add_files(files_instances=files_instances, post_instance=post_instance)

            PostCreateUpdateProcessor.set_categories(request=self.request, post_instance=post_instance)

            self._set_response(data={'message': 'Exito con la creación'}, status=status.HTTP_201_CREATED)

        else:
            self._set_response(data={'message': 'Información no válida'}, status=status.HTTP_400_BAD_REQUEST)