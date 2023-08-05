from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializer import MessageSerializer
from rest_framework.response import Response
from rest_framework import status
from posts_app.models import PostModel
from .models import MessagesModel
from api.serializers import MessageBaseSerializer

class MessageView(APIView):
    permission_classes = [permissions.IsAuthenticated] 
    authentication_classes = [JWTAuthentication]

    def post(self, request, id):
        message_serializer = MessageSerializer(data=request.data)
        
        if message_serializer.is_valid():
            message = message_serializer.create(validated_data=message_serializer.validated_data, user=request.user)
            post = PostModel.objects.get(id=id)
            post.messages.add(message)
            message_serializer = MessageBaseSerializer(instance=message)
            return Response(message_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response({'message': 'Problemas con la creación'}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        message_serializer = MessageSerializer(data=request.data)

        if message_serializer.is_valid():
            message_instance = MessagesModel.objects.get(id=request.data['id'])
            message = message_serializer.update(instance=message_instance, validated_data=message_serializer.validated_data)
            message_serializer = MessageBaseSerializer(instance=message)
            return Response(message_serializer.data, status=status.HTTP_200_OK)
        
        return Response({'error': 'Problemas con los datos enviados'}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, id):
        try:
            message = MessagesModel.objects.get(id=id)
            message_serializer = MessageSerializer(message, many=False, fields=['title', 'content'])
            return Response(message_serializer.data)
        except:
            return Response({'error': 'Mensaje no encontrado'})


