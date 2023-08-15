from rest_framework.response import Response
from django.db.models import Model
from api.classes.controller_logic_excecutor import ControllerLogicExecutor
from api.classes.access_data_logic_controller import AccessDataLogicController


def process_and_get_response(executor_base: ControllerLogicExecutor) -> Response:
    """
    Shortcut que se encargara de activar el proceso y devolver las respuesta
    """
    executor_base.start_process()
    return executor_base.response


def process_and_get_queryset(executor_base: AccessDataLogicController) -> Model:
    """
    Shortcut que se encargara de activar el proceso y devolver el queryset
    """
    executor_base.start_process()
    return executor_base.queryset
