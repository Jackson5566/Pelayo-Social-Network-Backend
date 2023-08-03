from .models import MessagesModel
from api.serializers import DynamicModelSerializer

class MessageSerializer(DynamicModelSerializer):
  class Meta:
    model = MessagesModel
    fields = ['title', 'content']

  def create(self, validated_data, user):
    instance = MessagesModel.objects.create(**validated_data, user=user)
    return instance
  
  