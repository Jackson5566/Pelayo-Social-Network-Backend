from typing import Union
from rest_framework import status
from api.classes.serializer_manager import SerializerManager
from api.classes.controller_logic_excecutor import ResponseBody
from posts_app.classes.posts_classes.bases.post_operations import PostOperations
from posts_app.serializer import PostsReturnSerializerWithoutUser, PostsReturnSerializerWithUser


class GetPostData(PostOperations):
    def __init__(self, request, post_id, context):
        super().__init__(request=request, model_id=post_id)
        self.context = context
        self.serializer_manager = SerializerManager()

    def start_process(self):
        data = self.get_data()
        self.response = ResponseBody(data=data, status=status.HTTP_200_OK)

    def get_data(self):
        return self.get_message_data() if self.show_only_messages() else self.get_post_data()

    def get_post_data(self):
        from_user = self.is_model_instance_from_user(user=self.authenticated_user)
        self.serialize_post(is_from_user=from_user)
        data = self.serializer_manager.serializer.data
        data['fromUser'] = from_user
        return data

    def get_message_data(self):
        self.serialize_without_user(fields=['messages'])
        data = self.serializer_manager.serializer.data
        return data

    def serialize_post(self, is_from_user: bool):
        self.serialize_without_user() if is_from_user else self.serialize_with_user()

    def serialize_without_user(self, fields: Union[list, None] = None) -> None:
        self.serializer_manager.serializer_class = PostsReturnSerializerWithoutUser(
            self.instance_manager.instance, many=False, context=self.context, fields=fields)

    def serialize_with_user(self) -> None:
        self.serializer_manager.serializer_class = PostsReturnSerializerWithUser(self.instance_manager.instance,
                                                                                 many=False, context=self.context)

    def show_only_messages(self) -> bool:
        return self.request_manager.request.query_params.get('onlyMessages') == 'true'
