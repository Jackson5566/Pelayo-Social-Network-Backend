from api.classes.controller_logic_excecutor import ControllerLogicExecutor
from api.classes.model_operations import ModelOperations
from posts_app.models import PostModel
from abc import ABC


class PostOperations(ControllerLogicExecutor, ModelOperations, ABC):

    def __init__(self, request, model_id=None):
        ControllerLogicExecutor.__init__(self, request=request)
        ModelOperations.__init__(self, model_id=model_id, model_class=PostModel)

    def is_post_from_authenticated_user(self, post_instance=None) -> bool:
        return self.request_manager.request.user == post_instance.user if post_instance \
            else self.request_manager.request.user == self.model_instance_manager.instance.user
