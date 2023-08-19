from ..models import User
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework import status
from api.classes.controller_logic_excecutor import ControllerLogicExecutor, ResponseBody
from api.classes.model_operations import ModelOperations, SearchModel
from api.classes.type_alias.operations import Operations


class DenunciateUser(Operations):
    def __init__(self, request):
        ControllerLogicExecutor.__init__(self, request=request)
        user_id = self.request_manager.request.data.get('id')
        ModelOperations.__init__(self, SearchModel(model_id=user_id, model_class=User))
        self.user_who_reported = self.request_manager.request.user

    def start_process(self) -> None:
        complain_error: Response = self.verify_complain()
        if not complain_error:
            self.add_complaint()
            self.verify_user_reported_complaints()
            self.response: ResponseBody = ResponseBody(data={'message': 'Usuario Denunciado'},
                                                       status=status.HTTP_200_OK)

    def verify_complain(self) -> Response:
        if self.user_who_reported not in self.instance_manager.instance.denunciations.all():
            if self.user_who_reported == self.instance_manager.instance:
                self.response = ResponseBody(data={'message': 'No puedes denunciarte'},
                                             status=status.HTTP_400_BAD_REQUEST)
        else:
            self.response = ResponseBody(data={'message': 'Usuario ya denunciado'}, status=status.HTTP_400_BAD_REQUEST)

        return self.response

    def add_complaint(self) -> None:
        self.instance_manager.instance.denunciations.add(self.user_who_reported)

    def verify_user_reported_complaints(self):
        user_reported_denuncations: int = self.count_user_reported_complaints()
        if user_reported_denuncations >= 20:
            self.send_complaint_mail(user_reported_denuncations=user_reported_denuncations)

    def count_user_reported_complaints(self) -> int:
        user_reported_denuncations: int = self.instance_manager.instance.denunciations.count()
        return user_reported_denuncations

    @staticmethod
    def send_complaint_mail(user_reported_denuncations: int) -> None:
        send_mail("Exceso de denuncias", f"El usuario ha sido denunciado {user_reported_denuncations} veces",
                  None, ["jackson0102almeida@gmail.com"])
