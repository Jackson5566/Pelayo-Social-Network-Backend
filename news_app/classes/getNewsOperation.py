from api.classes.controller_logic_excecutor import ResponseBody
from api.classes.serialzer_operations import SerializerOperations
from api.classes.type_alias.operations import GetProcessor
from news_app.classes.bases.newsOperations import NewsOperations
from news_app.serializers import GetNewsSerializer
from rest_framework import status


class GetNewsOperation(NewsOperations, GetProcessor):
    def __init__(self, request, news_instance):
        NewsOperations.__init__(self, request=request, model_instance=news_instance)
        SerializerOperations.__init__(self)

    def _get_serializer(self, **kwargs):
        return GetNewsSerializer(instance=self.instance_manager.instance, many=True)

    def start_process(self):
        data = self.serializer_manager.serializer.data
        self.response = ResponseBody(data=data, status=status.HTTP_200_OK)
