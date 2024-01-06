import argparse


# A programar mas coño

def generate_operations_class(nombre_archivo):
    codigo_predefinido = """
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

    with open(nombre_archivo + "_operations.py", "w") as archivo:
        archivo.write(codigo_predefinido)


def generate_createupdateoperations_class(nombre_archivo):
    codigo_predefinido = """
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

    with open(nombre_archivo + "_create_update_operations.py", "w") as archivo:
        archivo.write(codigo_predefinido)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generar un script con código predefinido.")
    parser.add_argument("nombre_archivo", help="Nombre del archivo de script a generar")
    parser.add_argument("to")
    args = parser.parse_args()
    if args.to == "operations":
        generate_operations_class(args.nombre_archivo)
    else:
        generate_createupdateoperations_class(args.nombre_archivo)
