from abc import ABC

from api.classes.serialzer_operations import SerializerOperations
from api.classes.type_alias.operations import CreateUpdateProcessor
from api.decorators.validate_serializer import validate_serializer
from posts_app.classes.posts_classes.bases.content_operations import ContentListOperations
from posts_app.serializer import CreateContentListSerializer


class ContentListCrUpOpr(ContentListOperations, CreateUpdateProcessor, ABC):

    def __init__(self, request, model_id=None):
        ContentListOperations.__init__(self, request=request, model_id=model_id)
        SerializerOperations.__init__(self)

    def _get_serializer(self, **kwargs):
        return CreateContentListSerializer(data=self.request_manager.request.data,
                                           context={'request': self.request_manager.request})

    @validate_serializer('serializer_manager')
    def start_process(self):
        self.create_or_update_process()
