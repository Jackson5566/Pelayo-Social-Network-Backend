from abc import ABC
from .request_manager import RequestManager
from .excecutor_base import ExecutorBase


class AccessDataLogicController(ExecutorBase, ABC):
    """Clase controladora del acceso a data(queryset)
    Propósito: Manejar las solicitudes, procesarlas y devolver un queryset
    """
    def __init__(self, request):
        self.request_manager = RequestManager(request=request)
        self._queryset = None

    @property
    def queryset(self):
        return self._queryset

    @queryset.setter
    def queryset(self, queryset):
        self._queryset = queryset
