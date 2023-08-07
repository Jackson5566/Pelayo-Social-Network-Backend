from typing import Union
from posts_app.serializer import PostsReturnSerializerWithoutUser, PostsReturnSerializerWithUser
from .post_base import PostBase
from rest_framework import status


class GetPostData(PostBase):
    def __init__(self, request, post_instance, context):
        super().__init__(request=request)
        self.post = post_instance
        self.context = context
        self.post_serializer = None

    def start_get_post_data_process(self):
        self._set_response(data=self.get_post_data(), status=status.HTTP_200_OK)

    def get_post_data(self):
        if self.show_only_messages():
            self.serialize_without_user(fields=['message'])
        else:
            if self.post.user == self.post.user:
                self.serialize_without_user(fields=None)
                from_user = True
            else:
                self.serialize_with_user()
                from_user = False

            info = self.post_serializer.data
            info['fromUser'] = from_user
            return info

    def serialize_without_user(self, fields: Union[list, None]) -> None:
        self.post_serializer = PostsReturnSerializerWithoutUser(self.post, many=False, context=self.context,
                                                                fields=fields)

    def serialize_with_user(self) -> None:
        self.post_serializer = PostsReturnSerializerWithUser(self.post, many=False, context=self.context)

    def show_only_messages(self) -> bool:
        return self.request.query_params.get('onlyMessages') == 'true'
