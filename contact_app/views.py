from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from .classes.send_mail import SendMailOperation
from api.shortcuts.data_get import process_and_get_response
from rest_framework_simplejwt.authentication import JWTAuthentication


class SendMail(APIView):
    authentication_classes = [JWTAuthentication]

    @extend_schema(
        responses={200: str, 404: str},
    )
    def post(self, request):
        send_mail_operation = SendMailOperation(request=request)
        return process_and_get_response(send_mail_operation)
