from typing import Union
from posts_app.serializer import PostsReturnSerializerWithoutUser, PostsReturnSerializerWithUser


class GetPostData:
    def __init__(self, request, post_instance, context):
        self.post = post_instance
        self.context = context
        self.request = request
        self.post_serializer = None

    def get_post_data(self):
        if self.show_only_messages():
            self.serialize_without_user(fields=['message'])
        else:
            if self.post.user == self.post.user:
                self.serialize_without_user(fields='__all__')
                from_user = True
            else:
                self.serialize_with_user()
                from_user = False

            info = self.post_serializer.data
            info['fromUser'] = from_user
            return info

    def serialize_without_user(self, fields: Union[list, str]) -> None:
        self.post_serializer = PostsReturnSerializerWithoutUser(self.post, many=False, context=self.context,
                                                                fields=fields)

    def serialize_with_user(self) -> None:
        self.post_serializer = PostsReturnSerializerWithUser(self.post, many=False, context=self.context)

    def show_only_messages(self) -> bool:
        return self.request.query_params.get('onlyMessages') == 'true'
