from api.classes.controller_logic_excecutor import ControllerLogicExecutor
from api.classes.model_operations import ModelOperations
from api.classes.instance_manager import InstanceManager
from abc import ABC


class PostOperations(ControllerLogicExecutor, ModelOperations, ABC):

    def __init__(self, request, model_id=None):
        super().__init__(request=request)
        post_instance = self.get_default_instance(model_id=model_id)
        self.post_instance_manager = InstanceManager(instance=post_instance)

    def is_post_from_authenticated_user(self, post_instance=None) -> bool:
        return self.request_manager.request.user == post_instance.user if post_instance \
            else self.request_manager.request.user == self.post_instance_manager.instance.user
