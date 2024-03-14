from . import file_extensions


class Generator(object):
    @staticmethod
    def generate_code(file_name, extension: str, code: str):
        with open(file_name + "_" + extension, "w") as archivo:
            archivo.write(code)


def generate_create_update_operation(file_name: str):
    code = """
from abc import ABC
from api.classes.controller_logic_excecutor import ControllerLogicExecutor
from api.classes.model_operations import ModelOperations, SearchModel
from api.classes.type_alias.operations import Operations
from news_app.models import NewsModel


class AppOperations(Operations, ABC):
    def __init__(self, request, model_id=None, model_instance=None):
        ControllerLogicExecutor.__init__(self, request=request)
        ModelOperations.__init__(self, SearchModel(model_id=model_id, model_class=NewsModel),
                                 model_instance=model_instance)
        """
    Generator.generate_code(file_name, file_extensions.OPERATIONS, code)


def generate_operations(file_name: str):
    code = """
from api.classes.serialzer_operations import SerializerOperations
from api.classes.type_alias.operations import CreateUpdateProcessor
from api.decorators.validate_serializer import validate_serializer
from news_app.classes.bases.newsOperations import NewsOperations
from news_app.serializers import CreateNewsSerializer


class AppCreateUpdateOperations(AppOperations, CreateUpdateProcessor):

    def __init__(self, request, model_id=None):
        NewsOperations.__init__(self, request=request, model_id=model_id)
        SerializerOperations.__init__(self)

    def _get_serializer(self, **kwargs):
        return CreateNewsSerializer(data=self.request_manager.request.data)

    @validate_serializer('serializer_manager')
    def start_process(self):
        self.create_or_update_process()
        """

    Generator.generate_code(file_name, file_extensions.CREATE_UPDATE_OPERATIONS, code)
