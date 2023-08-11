from abc import ABC, abstractmethod
from rest_framework.response import Response


class ViewLogicExecutor(ABC):
    def __init__(self, request):
        self.request = request
        self._response = None

    @property
    def response(self):
        return self._response

    def _set_response(self, **kwargs) -> None:
        self._response = Response(**kwargs)

    @abstractmethod
    def start_process(self) -> None:
        pass
