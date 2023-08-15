from abc import ABC
from api.classes.instance_manager import InstanceManager
from api.classes.controller_logic_excecutor import ControllerLogicExecutor
from api.classes.model_operations import ModelOperations


class CommentOperations(ControllerLogicExecutor, ModelOperations, ABC):
    """Esta clase abarca las operaciones relacionadas con la app de comment
    Propósito: Expander ControllerLógic Excecutor, para lograr una personalización y compartir metodos, atributos entre
    las clases que hereden de esta"""
    def __init__(self, request, model_id=None):
        super().__init__(request=request)
        comment_instance = self.get_default_instance(model_id=model_id)
        self.comment_instance_manager = InstanceManager(instance=comment_instance)
