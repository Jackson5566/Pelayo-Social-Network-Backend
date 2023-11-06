from abc import ABC

from api.classes.serialzer_operations import SerializerOperations
from api.classes.type_alias.operations import CreateUpdateProcessor
from api.decorators.validate_serializer import validate_serializer
from news_app.classes.bases.newsOperations import NewsOperations
from news_app.serializers import CreateNewsSerializer


class NewsCreateUpdateOperations(NewsOperations, CreateUpdateProcessor, ABC):

    def __init__(self, request, model_id=None):
        NewsOperations.__init__(self, request=request, model_id=model_id)
        SerializerOperations.__init__(self)

    def _get_serializer(self, **kwargs):
        return CreateNewsSerializer(data=self.request_manager.request.data)

    @validate_serializer('serializer_manager')
    def start_process(self):
        self.create_or_update_process()
