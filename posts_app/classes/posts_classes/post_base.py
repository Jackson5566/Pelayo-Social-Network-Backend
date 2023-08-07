from abc import ABC, abstractmethod
from rest_framework.response import Response


class PostBase(ABC):
    def __init__(self, request):
        self.request = request
        self._response = None

    @property
    def response(self):
        return self._response

    def _set_response(self, **kwargs):
        self._response = Response(**kwargs)


class PostCreateUpdateBase(ABC):
    def __init__(self):
        self.post_serializer = self._get_serializer_post()

    @abstractmethod
    def _get_serializer_post(self):
        pass
