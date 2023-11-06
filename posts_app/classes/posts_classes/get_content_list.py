from rest_framework import status
from api.classes.controller_logic_excecutor import ResponseBody
from posts_app.classes.posts_classes.bases.content_operations import ContentListOperations
from posts_app.models import ContentListModel
from posts_app.serializer import GetContentListSerializer
from api.classes.serialzer_operations import SerializerOperations


class GetContentList(ContentListOperations, SerializerOperations):

    def __init__(self, request):
        ContentListOperations.__init__(self, request=request)
        SerializerOperations.__init__(self)

    def _get_serializer(self, **kwargs):
        id = self.request_manager.request.query_params.get('user__id')
        queryset = ContentListModel.objects.filter(user__id=id)
        return GetContentListSerializer(instance=queryset, many=True)

    def start_process(self):
        data = self.serializer_manager.serializer.data
        self.response = ResponseBody(data=data, status=status.HTTP_200_OK)
