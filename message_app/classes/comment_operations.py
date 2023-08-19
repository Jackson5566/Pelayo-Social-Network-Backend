from abc import ABC
from message_app.models import MessagesModel
from api.classes.model_operations import ModelOperations, SearchModel
from api.classes.controller_logic_excecutor import ControllerLogicExecutor
from api.classes.type_alias.operations import Operations


class CommentOperations(Operations, ABC):
    """Esta clase abarca las operaciones relacionadas con la app de comment
    Propósito: Expander ControllerLógic Excecutor, para lograr una personalización y compartir metodos, atributos entre
    las clases que hereden de esta"""

    def __init__(self, request, model_id=None):
        ControllerLogicExecutor.__init__(self, request=request)
        ModelOperations.__init__(self, search_model=SearchModel(model_id=model_id, model_class=MessagesModel))

