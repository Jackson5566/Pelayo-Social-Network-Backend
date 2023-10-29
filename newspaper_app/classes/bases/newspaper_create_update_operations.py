from api.classes.serialzer_operations import SerializerOperations
from api.classes.type_alias.operations import CreateUpdateProcessor
from api.decorators.validate_serializer import validate_serializer
from newspaper_app.classes.bases.newspaperOperations import NewspaperOperations
from newspaper_app.serializer import CreateNewspaperSectionSerializer


class NewspaperCreateUpdateOperations(NewspaperOperations, CreateUpdateProcessor):

    def __init__(self, request, model_id=None):
        NewspaperOperations.__init__(self, request=request, model_id=model_id)
        SerializerOperations.__init__(self)

    def _get_serializer(self, **kwargs):
        return CreateNewspaperSectionSerializer(data=self.request_manager.request.data)

    @validate_serializer('serializer_manager')
    def start_process(self):
        self.create_or_update_process()
