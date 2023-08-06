from rest_framework.exceptions import ValidationError
from posts_app.classes.posts_classes.post_processor import PostProcessor
from .post_base import PostCreateUpdateBase
from posts_app.serializer import PostsCreateSerializer


class CreatePost(PostCreateUpdateBase):
    def __init__(self, request):
        super().__init__(request=request)

    def _get_serializer_post(self):
        return PostsCreateSerializer(data=self.request.data, scontext={'request': self.request})

    def create_post(self):
        files_instances = PostProcessor.serialize_files(self.request)
        if self.post_serializer.is_valid():
            post_instance = self.post_serializer.create(validated_data=self.post_serializer.validated_data)

            PostProcessor.add_files(files_instances=files_instances, post_instance=post_instance)

            PostProcessor.set_categories(request=self.request, post_instance=post_instance)

        else:
            raise ValidationError("No válido")
