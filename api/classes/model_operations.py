from django.db.models import Model
from api.classes.instance_manager import InstanceManager
from django.shortcuts import get_object_or_404
from dataclasses import dataclass
from typing import Union, Type


@dataclass
class SearchModel:
    model_id: int
    model_class: Type[Model]


class ModelOperations:
    """
    Clase que trabaja con una instancia del modelo y que además va obtener la instancia mediante un id pasado como
    parámetro
    """

    def __init__(self, search_model: Union[SearchModel, None] = None, model_instance=None):
        if not search_model and not model_instance:
            raise Exception("Informacion no enviada")

        default_model_instance = get_object_or_404(search_model.model_class, id=search_model.model_id) if (
            search_model) else model_instance

        self.instance_manager = InstanceManager(instance=default_model_instance)

    def is_model_instance_from_user(self, user) -> bool:
        return user == self.instance_manager.instance.user
