from abc import ABC
from api.classes.controller_logic_excecutor import ControllerLogicExecutor
from api.classes.model_operations import ModelOperations, SearchModel
from api.classes.type_alias.operations import Operations
from newspaper_app.models import NewspaperModel


class NewspaperOperations(Operations, ABC):
    def __init__(self, request, model_id=None, model_instance=None):
        ControllerLogicExecutor.__init__(self, request=request)
        ModelOperations.__init__(self, SearchModel(model_id=model_id, model_class=NewspaperModel),
                                 model_instance=model_instance)