from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str
from django.core.signing import TimestampSigner, BadSignature
from django.template.loader import render_to_string
from django.core.mail import send_mail
from ..models import User
from rest_framework.response import Response
from rest_framework import status
from typing import Union

# Analizar funcionamiento

class EncodeProccesor:
    @staticmethod
    def encode(token):
        encoded_token = urlsafe_base64_encode(token.encode())
        return encoded_token

    @staticmethod
    def decode(token):
        decode_token = urlsafe_base64_decode(token)
        decoded_token_str = force_str(decode_token)
        return decoded_token_str


class UserExpirationLinkUtilities:
    def __init__(self):
        self.signer = TimestampSigner()
        self._user = None

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        self._user = user

class SendUserExpirationLink:
    FRONT_END_SITE = 'pelayo-social-network.web.app'

    def __init__(self):
        self.utilities = UserExpirationLinkUtilities()

    def send_link(self, template: str, subject: str) -> None:
        if self.utilities.user:
            encoded_token = self.encode_token()
            message = render_to_string(template, {
                'user': self.utilities.user,
                'domain': self.FRONT_END_SITE,
                'token': encoded_token,
            })
            print("Ususario: " + self.utilities.user.email)
            send_mail(subject, "Registro de usuario: ", None,
                      [self.utilities.user.email],
                      fail_silently=False, html_message=message)

    def encode_token(self) -> str:
        token = self.utilities.signer.sign(str(self.utilities.user.id))
        return EncodeProccesor.encode(token=token)


class GetUserFromExpirationLink:

    def __init__(self):
        self.utilities = UserExpirationLinkUtilities()

    def set_user(self, token: str) -> Union[Response, None]:
        decoded_token_str = self.decode_token(token)
        user_id = self.utilities.signer.unsign(decoded_token_str, max_age=3600)
        try:
            self.utilities.user = User.objects.get(id=int(user_id))
        except BadSignature:
            return Response({'error': 'Link de resto inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Usario no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def decode_token(self, token):
        return EncodeProccesor.decode(token=token)
