from typing import Union

from api.classes.view_logic_executor import ResponseBody
from posts_app.classes.posts_classes.bases.post_operations import PostOperations
from posts_app.serializer import PostsReturnSerializerWithoutUser, PostsReturnSerializerWithUser
from rest_framework import status


class GetPostData(PostOperations):
    def __init__(self, request, post_instance, context):
        super().__init__(request=request, post_instance=post_instance)
        self.context = context
        self.post_serializer = None

    def start_process(self):
        data = self.get_data()
        self.response = ResponseBody(data=data, status=status.HTTP_200_OK)

    def get_data(self):
        return self.get_message_data() if self.show_only_messages() else self.get_post_data()

    def get_post_data(self):
        from_user = self.is_post_from_authenticated_user()
        self.serialize_post(is_from_user=from_user)
        data = self.post_serializer.data
        data['fromUser'] = from_user
        return data

    def get_message_data(self):
        self.serialize_without_user(fields=['message'])
        data = self.post_serializer.data
        return data

    def serialize_post(self, is_from_user: bool):
        self.serialize_without_user() if is_from_user else self.serialize_with_user()

    def serialize_without_user(self, fields: Union[list, None] = None) -> None:
        self.post_serializer = PostsReturnSerializerWithoutUser(self.post_instance, many=False, context=self.context,
                                                                fields=fields)

    def serialize_with_user(self) -> None:
        self.post_serializer = PostsReturnSerializerWithUser(self.post_instance, many=False, context=self.context)

    def show_only_messages(self) -> bool:
        return self.request_manager.request.query_params.get('onlyMessages') == 'true'
