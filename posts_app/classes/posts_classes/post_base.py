from abc import ABC, abstractmethod


class PostCreateUpdateBase(ABC):
    def __init__(self, request):
        self.request = request
        self.post_serializer = self._get_serializer_post()

    @abstractmethod
    def _get_serializer_post(self):
        pass
