from abc import ABC

from ..models import User
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework import status
from typing import Union
from api.classes.view_logic_executor import ViewLogicExecutor


class DenunciateUser(ViewLogicExecutor):
    def __init__(self, request):
        super().__init__(request=request)
        self.user_who_reported = self.request.user
        self.user_reported = self.get_user_reported()

    def get_user_reported(self) -> User:
        try:
            user_reported_id = self.request.get('id')
            return User.objects.filter(id=user_reported_id).first()
        except User.DoesNotExist:
            self._set_response(data={'message': 'Usuario no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def start_process(self) -> None:
        complain_error = self.verify_complain()
        if complain_error is None:
            self.add_complaint()
            self.verify_user_reported_complaints()
            self._set_response(data={'message': 'Usuario Denunciado'}, status=status.HTTP_200_OK)

    def verify_complain(self) -> Response:
        if self.user_who_reported not in self.user_reported.denunciations.all():
            if self.user_who_reported == self.user_reported:
                self._set_response(data={'message', 'No puedes denunciarte'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            self._set_response(data={'message': 'Usuario ya denunciado'}, status=status.HTTP_400_BAD_REQUEST)

        return self.response

    def add_complaint(self) -> None:
        self.user_reported.denunciations.add(self.user_who_reported)

    def verify_user_reported_complaints(self):
        user_reported_denuncations = self.count_user_reported_complaints()
        if user_reported_denuncations >= 20:
            self.send_complaint_mail(user_reported_denuncations=user_reported_denuncations)

    def count_user_reported_complaints(self) -> int:
        user_reported_denuncations = self.user_reported.denunciations.count()
        return user_reported_denuncations

    @staticmethod
    def send_complaint_mail(user_reported_denuncations: int) -> None:
        send_mail("Exceso de denuncias", f"El usuario ha sido denunciado {user_reported_denuncations} veces",
                  None, ["jackson0102almeida@gmail.com"])
