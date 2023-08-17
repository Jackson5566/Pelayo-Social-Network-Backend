from abc import ABC
from auth_app.models import User
from api.classes.model_operations import ModelOperations
from api.classes.type_alias.operations import Operations
from api.classes.controller_logic_excecutor import ControllerLogicExecutor


class UserOperations(Operations, ABC):
    def __init__(self, request, model_id=None, model_instance=None):
        ControllerLogicExecutor.__init__(self, request=request)
        ModelOperations.__init__(self, model_id=model_id, model_instance=model_instance, model_class=User)

    def only_post(self) -> bool:
        return self.request_manager.request.query_params.get('onlyPosts') == 'true'

    def only_information(self) -> bool:
        return self.request_manager.request.query_params.get('onlyInformation') == 'true'
