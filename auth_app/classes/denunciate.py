from ..models import User
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework import status
from typing import Union


class DenunciateUser:
    user_reported = None

    def __init__(self, user_who_reported, user_reported_id):
        self.user_who_reported = user_who_reported
        self.set_user_reported(user_reported_id)

    def set_user_reported(self, user_reported_id: int) -> Union[Response, None]:
        try:
            self.user_reported = User.objects.filter(id=user_reported_id).first()
        except User.DoesNotExist:
            return Response({'message': 'Usuario no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def start_denunciate_proccess(self) -> Response:
        complain_error = self.verify_complain()
        if complain_error:
            return complain_error
        else:
            self.add_complaint()
            user_reported_denuncations = self.count_user_reported_complaints()
            if user_reported_denuncations >= 20:
                self.send_complaint_mail(user_reported_denuncations=user_reported_denuncations)
            return Response("Usario denunciado", status=status.HTTP_200_OK)

    def verify_complain(self) -> Union[Response, None]:
        if self.user_who_reported not in self.user_reported.denunciations.all():
            if self.user_who_reported == self.user_reported:
                return Response({'message', 'No puedes denunciarte'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response('Usuario ya denunciado', status=status.HTTP_400_BAD_REQUEST)

    def add_complaint(self) -> None:
        self.user_reported.denunciations.add(self.user_who_reported)

    def count_user_reported_complaints(self) -> int:
        user_reported_denuncations = self.user_reported.denunciations.count()
        return user_reported_denuncations

    @staticmethod
    def send_complaint_mail(user_reported_denuncations: int) -> None:
        send_mail("Exceso de denuncias", f"El usuario ha sido denunciado {user_reported_denuncations} veces",
                  None, ["jackson0102almeida@gmail.com"])
