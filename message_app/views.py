from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import MessageSerializer
from rest_framework.response import Response
from .models import MessagesModel
from message_app.classes.create_comment import CreateCommentOperation


class MessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        create_comment_instance = CreateCommentOperation(request=request)
        create_comment_instance.start_process()
        return create_comment_instance.response

    def put(self, request):
        update_comment_instance = CreateCommentOperation(request=request)
        update_comment_instance.start_process()
        return update_comment_instance.response

    def get(self, request, id):
        try:
            message = MessagesModel.objects.get(id=id)
            message_serializer = MessageSerializer(message, many=False, fields=['title', 'content'])
            return Response(message_serializer.data)
        except:
            return Response({'error': 'Mensaje no encontrado'})
