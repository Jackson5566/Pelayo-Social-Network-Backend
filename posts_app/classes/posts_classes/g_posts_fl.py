from rest_framework import status
from api.classes.controller_logic_excecutor import ResponseBody
from posts_app.classes.posts_classes.bases.content_operations import ContentListOperations
from posts_app.serializer import GetContentListSerializer, PostsReturnSerializerWithoutUser
from api.classes.serialzer_operations import SerializerOperations


class GetPostsFL(ContentListOperations, SerializerOperations):

    def __init__(self, request, content_list_id):
        ContentListOperations.__init__(self, request=request, model_id=content_list_id)
        SerializerOperations.__init__(self)

    def _get_serializer(self, **kwargs):
        posts = self.instance_manager.instance.posts.all()
        return PostsReturnSerializerWithoutUser(instance=posts, many=True)

    def start_process(self):
        data = self.serializer_manager.serializer.data
        self.response = ResponseBody(data=data, status=status.HTTP_200_OK)
