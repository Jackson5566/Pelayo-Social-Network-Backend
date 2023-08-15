from abc import ABC, abstractmethod
from typing import Union
from django.db.models import Model


class ModelOperations(ABC):
    @abstractmethod
    def get_default_instance(self, model_id=None) -> Union[None, Model]:
        pass
