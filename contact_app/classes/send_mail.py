from smtplib import SMTPException
from rest_framework import status
from django.core.mail import send_mail
from api.classes.controller_logic_excecutor import ControllerLogicExecutor, ResponseBody
from api.classes.serialzer_operations import SerializerOperations
from contact_app.serializer import ContactSerializer
from api.decorators.validate_serializer import validate_serializer


class SendMailOperation(ControllerLogicExecutor, SerializerOperations):
    def __init__(self, request):
        ControllerLogicExecutor.__init__(self, request=request)
        SerializerOperations.__init__(self)

    def _get_serializer(self, **kwargs):
        return ContactSerializer(data=self.request_manager.request.data)

    @validate_serializer('serializer_manager')
    def start_process(self):
        data = self.serializer_manager.serializer.validated_data
        user = self.request_manager.request.user
        try:
            # user.email if user.is_authenticated else data['email']}
            send_mail(data['subject'], data['content'] +
                      f"\nEmail enviado por: {data['email']}",
                      "jackson0102almeida@gmail.com", ["jackson0102almeida@gmail.com"],
                      fail_silently=False)
            self.response = ResponseBody(data={"info": "Mail enviado correctamente"}, status=status.HTTP_200_OK)
        except SMTPException:
            self.response = ResponseBody(data={"info": "Ha ocurrido un error con el envio del mail"},
                                         status=status.HTTP_406_NOT_ACCEPTABLE)
