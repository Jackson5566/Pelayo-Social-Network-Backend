from django.core.mail import send_mail
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework import permissions
from .serializer import ContactSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
@authentication_classes([JWTAuthentication])
def fsend_mail(request):
    serializer = ContactSerializer(data=request.data)
    if serializer.is_valid():
      data = serializer.validated_data
      try:
        send_mail( data['subject'], data['content'] + f"Email enviado por: {request.user.email if request.user.is_authenticated else data['email']}", "jackson0102almeida@gmail.com", ["jackson0102almeida@gmail.com"], fail_silently=False)
        return Response({"info": "Mail enviado correctamente"})
      except:
        return Response({"info": "Ha ocurrido un error con el envio del mail"}, status=status.HTTP_406_NOT_ACCEPTABLE)
      
    return Response({"info": "No es valido"}, status=status.HTTP_400_BAD_REQUEST)