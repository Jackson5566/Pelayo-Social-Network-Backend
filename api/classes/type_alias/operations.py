from api.classes.controller_logic_excecutor import ControllerLogicExecutor
from api.classes.create_update_proccesor import CreateUpdate
from api.classes.model_operations import ModelOperations
from abc import ABC, abstractmethod
from api.classes.serialzer_operations import SerializerOperations


class Operations(ControllerLogicExecutor, ModelOperations, ABC):
    pass


class CreateUpdateProcessor(CreateUpdate, SerializerOperations, ABC):
    pass


class DeleteProcessor(ABC):
    @abstractmethod
    def delete(self):
        pass
