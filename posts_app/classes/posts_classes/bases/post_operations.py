from abc import ABC

from api.classes.controller_logic_excecutor import ControllerLogicExecutor
from api.classes.model_operations import ModelOperations, SearchModel
from posts_app.models import PostModel
from api.classes.type_alias.operations import Operations


class PostOperations(Operations, ABC):

    def __init__(self, request, model_id=None, model_instance=None):
        ControllerLogicExecutor.__init__(self, request=request)
        ModelOperations.__init__(self, SearchModel(model_id=model_id, model_class=PostModel),
                                 model_instance=model_instance)
        self.authenticated_user = self.request_manager.request.user

    # def is_model_from_authenticated_user(self, post_instance=None) -> bool:
    #     return self.request_manager.request.user == post_instance.user if post_instance \
    #         else self.request_manager.request.user == self.model_instance_manager.instance.user
