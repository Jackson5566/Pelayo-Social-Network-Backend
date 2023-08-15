from .models import MessagesModel
from api.serializers import DynamicModelSerializer


class CommentSerializer(DynamicModelSerializer):
    class Meta:
        model = MessagesModel
        fields = ['title', 'content']

    def create(self, validated_data):
        instance = MessagesModel.objects.create(**validated_data, user=self.context.get('request').user)
        return instance
