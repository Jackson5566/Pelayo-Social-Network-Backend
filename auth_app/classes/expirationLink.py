from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_str  
from django.core.signing import TimestampSigner, BadSignature
from django.template.loader import render_to_string
from django.core.mail import send_mail
from ..models import User
from rest_framework.response import Response
from rest_framework import status

class UserExpirationLink:
    frontEnd_site = 'localhost:4200'
    subject = 'Password Reset Request'
    signer = TimestampSigner()

    def encode_token(self):
        token = self.signer.sign(str(self.user.id))
        encoded_token = urlsafe_base64_encode(token.encode())
        return encoded_token
    
    def decode_token(self, token):
        decode_token = urlsafe_base64_decode(token)
        decoded_token_str = force_str(decode_token)
        return decoded_token_str

    def send_link(self, template: str) -> None:
        if self.user:
            encoded_token = self.encode_token()
            message = render_to_string(template, {
                'user': self.user,
                'domain': self.frontEnd_site,
                'token': encoded_token,
            })
            send_mail(self.subject, None, None, [self.email], fail_silently=False, html_message=message)

    def set_user(self, token: str) -> None:
        decoded_token_str = self.decode_token(token)
        user_id = self.signer.unsign(decoded_token_str, max_age=3600)
        try:
            self.user = User.objects.get(id=int(user_id))
        except BadSignature:
            return Response({'error': 'Link de reseto inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'error': 'Usario no encontrado'}, status=status.HTTP_400_BAD_REQUEST)