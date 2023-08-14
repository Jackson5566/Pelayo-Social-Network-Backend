from rest_framework import status
from api.classes.view_logic_executor import ResponseBody
from posts_app.classes.posts_classes.bases.post_operations import PostOperations


class DeletePost(PostOperations):
    def __init__(self, request, post_instance):
        super().__init__(request=request, post_instance=post_instance)

    def start_process(self):
        self.delete_post()
        self.response = ResponseBody(data={'message': 'Deleted'}, status=status.HTTP_200_OK)

    def delete_post(self):
        self.post_instance.delete()
