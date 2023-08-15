from django.db.models import Model
from typing import Union


class InstanceManager:
    """Clase encargada de administrar las instancias de los modelos que se usan en las clases"""

    def __init__(self, instance: Union[Model, None] = None):
        self._instance = instance

    @property
    def instance(self):
        return self._instance

    @instance.setter
    def instance(self, instance):
        self._instance = instance
