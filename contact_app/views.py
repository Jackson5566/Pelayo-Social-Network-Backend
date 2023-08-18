from rest_framework.views import APIView
from api.decorators.add_security import access_protected
from .classes.send_mail import SendMailOperation
from api.shortcuts.data_get import process_and_get_response


@access_protected
class SendMail(APIView):
    def post(self, request):
        send_mail_operation = SendMailOperation(request=request)
        return process_and_get_response(send_mail_operation)
