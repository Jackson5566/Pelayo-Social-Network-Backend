from abc import ABC, abstractmethod
from api.classes.serializer_manager import SerializerManager


class SerializerOperations(ABC):
    def __init__(self):
        post_serializer = self._get_serializer()
        self.serializer_manager = SerializerManager(serializer=post_serializer)

    @abstractmethod
    def _get_serializer(self):
        pass
