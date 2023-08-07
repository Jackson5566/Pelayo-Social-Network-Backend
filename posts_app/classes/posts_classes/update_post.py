from .post_base import PostCreateUpdateBase
from posts_app.serializer import PostsCreateSerializer
from posts_app.models import PostModel
from .post_processor import PostProcessor
from rest_framework.exceptions import ValidationError


class NotAllowed(Exception):
    def __init__(self, message):
        super().__init__(message)


class UpdatePost(PostCreateUpdateBase):
    def __init__(self, request):
        super().__init__(request=request)
        self.post_instance = None

    def _get_serializer_post(self):
        return PostsCreateSerializer(data=self.request.data)

    def start_update_post(self):
        files_instances = PostProcessor.serialize_files(request=self.request)

        if self.post_serializer.is_valid():
            post = PostModel.objects.get(id=self.request.data['id'])

            post.categories.clear()

            PostProcessor.set_categories(request=self.request, post_instance=post)

            if self.request.user == post.user:
                post_instance = self.post_serializer.update(validated_data=self.post_serializer.validated_data,
                                                            instance=post)

                PostProcessor.add_files(post_instance=post_instance, files_instances=files_instances)

            else:
                raise NotAllowed("No tienes permiso para esto")
        raise ValidationError("No válido")


"""posts_serializer = PostsCreateSerializer(data=request.data)

files_instances = PostProcessor.serialize_files(request=request)

if posts_serializer.is_valid():
    post = PostModel.objects.get(id=request.data['id'])

    post.categories.clear()

    PostProcessor.set_categories(request=request, post_instance=post)

    if request.user == post.user:
        post_instance = posts_serializer.update(validated_data=posts_serializer.validated_data, instance=post)

        PostProcessor.add_files(post_instance=post_instance, files_instances=files_instances)

        return Response({
            'message': 'Exito con la actualización'
        }, status=status.HTTP_200_OK)
    return Response({
        'message': 'No tienes permiso para realizar la actualización'
    }, status=status.HTTP_403_FORBIDDEN)

return Response({
    'message': 'Error con la actualización, información no válida'
}, status=status.HTTP_400_BAD_REQUEST)"""
