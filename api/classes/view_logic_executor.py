from abc import ABC

from rest_framework.response import Response
from dataclasses import dataclass
from .request_manager import RequestManager
from .excecutor_base import ExecutorBase


@dataclass
class ResponseBody:
    data: dict
    status: int


class ControllerLogicExecutor(ExecutorBase, ABC):
    """Ejecutor de la lógica del controlador"""

    def __init__(self, request):
        self.request_manager = RequestManager(request=request)
        self._response = None

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, response: ResponseBody) -> None:
        self._response = Response(data=response.data, status=response.status)