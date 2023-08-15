from api.classes.instance_manager import InstanceManager
from django.shortcuts import get_object_or_404


class ModelOperations:
    def __init__(self, model_id, model):
        default_model_instance = get_object_or_404(model, id=model_id) if model_id else None
        self.model_instance_manager = InstanceManager(instance=default_model_instance)
