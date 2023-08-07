from rest_framework.response import Response
from rest_framework import status
from .post_base import PostBase


class DeletePost(PostBase):
    def __init__(self, request, post_instance):
        super().__init__(request=request)
        self.post_instance = post_instance

    def start_delete_post_process(self):
        self.delete_post()
        self._set_response(data={'message': 'Delete'}, status=status.HTTP_200_OK)

    def delete_post(self):
        self.post_instance.delete()
