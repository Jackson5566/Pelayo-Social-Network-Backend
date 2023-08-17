from api.classes.controller_logic_excecutor import ControllerLogicExecutor
from api.classes.create_update_proccesor import CreateUpdateProcessor
from api.classes.model_operations import ModelOperations
from abc import ABC
from api.classes.serialzer_operations import SerializerOperations


class Operations(ControllerLogicExecutor, ModelOperations, ABC):
    pass


class CreateUpdateOperation(CreateUpdateProcessor, SerializerOperations, ABC):
    pass
