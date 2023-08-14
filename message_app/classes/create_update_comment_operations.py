from abc import ABC, abstractmethod
from api.classes.view_logic_executor import ControllerLogicExecutor, ResponseBody
from api.serializers import MessageBaseSerializer
from message_app.serializer import MessageSerializer
from rest_framework import status
from typing import Union
from ..models import MessagesModel


class CreateUpdateCommentOperations(ControllerLogicExecutor, ABC):
    def __init__(self, request):
        super().__init__(request=request)
        self._comment_serializer = self.get_message_serializer()
        self._message_instance = self.get_default_message_instance()

    def start_process(self) -> None:
        if self._comment_serializer.is_valid():
            self.create_or_update_process()
            self.set_created_message()

    @property
    def message_instance(self):
        return self._message_instance

    @property
    def comment_serializer(self):
        return self._comment_serializer

    @message_instance.setter
    def message_instance(self, message_instance: MessagesModel):
        self.message_instance = message_instance

    @abstractmethod
    def create_or_update_process(self) -> None:
        pass

    @abstractmethod
    def get_default_message_instance(self) -> Union[None, MessagesModel]:
        pass

    def set_created_message(self) -> None:  # Se estará viendo en response
        message_to_return_serializer = MessageBaseSerializer(instance=self._message_instance)
        self.response = ResponseBody(data=message_to_return_serializer.data, status=status.HTTP_201_CREATED)

    def get_message_serializer(self) -> MessageSerializer:
        return MessageSerializer(data=self.request_manager.data)