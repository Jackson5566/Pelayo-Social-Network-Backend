from abc import ABC
from message_app.models import MessagesModel
from api.classes.model_operations import ModelOperations
from api.classes.controller_logic_excecutor import ControllerLogicExecutor


class CommentOperations(ControllerLogicExecutor, ModelOperations, ABC):
    """Esta clase abarca las operaciones relacionadas con la app de comment
    Propósito: Expander ControllerLógic Excecutor, para lograr una personalización y compartir metodos, atributos entre
    las clases que hereden de esta"""

    def __init__(self, request, model_id=None):
        ControllerLogicExecutor.__init__(self, request=request)
        ModelOperations.__init__(self, model_id=model_id, model=MessagesModel)
