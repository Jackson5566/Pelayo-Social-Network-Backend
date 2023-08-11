from rest_framework import status
from posts_app.classes.posts_classes.bases.post_operations import PostOperations


class DeletePost(PostOperations):
    def __init__(self, request, post_instance):
        super().__init__(request=request, post_instance=post_instance)

    def start_process(self):
        self.delete_post()
        self._set_response(data={'message': 'Delete'}, status=status.HTTP_200_OK)

    def delete_post(self):
        self.post_instance.delete()
