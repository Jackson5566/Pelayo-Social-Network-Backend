from api.classes.controller_logic_excecutor import ControllerLogicExecutor
from api.classes.create_update_proccesor import CreateUpdate
from api.classes.model_operations import ModelOperations
from abc import ABC, abstractmethod
from api.classes.serialzer_operations import SerializerOperations


class Operations(ControllerLogicExecutor, ModelOperations, ABC):
    """
    Todas las operaciones se realizan sobre un modelo:
        - POST: instance, va a ser el objeto creado
        - GET: instance, va a ser el objeto recuperado de la base de datos
        - PUT: instance, va a ser el objeto actualizado
        - Delete: instance, va a ser el objeto eliminado
    """
    pass


class CreateUpdateProcessor(CreateUpdate, SerializerOperations, ABC):
    """
    Interfaz sobre operaciones de creación y actualización.
    Necesita un serializer
    """
    pass


class DeleteProcessor(ABC):
    """
    Interfaz para operaciones de eliminación
    """
    @abstractmethod
    def delete(self):
        pass


class GetProcessor(SerializerOperations, ABC):
    """
    Interfaz para operaciones de obtención de la base de datos
    """
    pass
