from typing import Union
from rest_framework import status
from api.classes.controller_logic_excecutor import ResponseBody
from posts_app.classes.posts_classes.bases.post_operations import PostOperations
from posts_app.serializer import PostsReturnSerializerWithoutUser, PostsReturnSerializerWithUser
from api.classes.serialzer_operations import SerializerOperations
from rest_framework.serializers import ModelSerializer


# Adaptacion del codigo a SerialzierOperations

class GetPostData(PostOperations, SerializerOperations):

    def __init__(self, request, post_id):
        PostOperations.__init__(self, request=request, model_id=post_id)
        self.context = {'request': request}
        # No me gusta, refactorizar
        self.is_from_user = self.is_model_instance_from_user(user=self.authenticated_user)
        self.only_messages = self.show_only_messages()
        SerializerOperations.__init__(self)

    def _get_serializer(self, **kwargs):
        serializer = self.serialize_without_user(fields=['messages']) if self.only_messages else self.serialize_post()
        return serializer

# ¿ form user?
    def start_process(self):
        data = self.serializer_manager.serializer.data

        if self.is_from_user:

            self.response = ResponseBody(data=data, status=status.HTTP_200_OK)

        else:
            self.response = ResponseBody(data={'message': "No permitido"}, status=status.HTTP_403_FORBIDDEN)

    def serialize_post(self) -> ModelSerializer:
        return self.serialize_without_user() if self.is_from_user else self.serialize_with_user()

    def serialize_without_user(self, fields: Union[list, None] = None) -> ModelSerializer:
        return PostsReturnSerializerWithoutUser(
            self.instance_manager.instance, many=False, context=self.context, fields=fields)

    def serialize_with_user(self) -> ModelSerializer:
        return PostsReturnSerializerWithUser(self.instance_manager.instance, many=False, context=self.context)

    def show_only_messages(self) -> bool:
        return self.request_manager.request.query_params.get('onlyMessages') == 'true'