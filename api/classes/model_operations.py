from api.classes.instance_manager import InstanceManager
from django.shortcuts import get_object_or_404


class ModelOperations:
    """
    Clase que trabaja con una instancia del modelo y que además va obtener la instancia mediante un id pasado como
    parámetro
    """
    def __init__(self, model_class, model_id=None, model_instance=None):
        default_model_instance = get_object_or_404(model_class, id=model_id) if model_id else model_instance
        self.instance_manager = InstanceManager(instance=default_model_instance)

    def is_model_instance_from_user(self, user) -> bool:
        return user == self.instance_manager.instance.user

