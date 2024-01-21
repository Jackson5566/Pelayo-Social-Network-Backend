import os

from rest_framework.serializers import ModelSerializer
from news_app.models import NewsModel


class GetNewsSerializer(ModelSerializer):
    class Meta:
        model = NewsModel
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['image'] = os.path.basename(instance.image.url) if instance.image else None
        return ret


class CreateNewsSerializer(ModelSerializer):
    class Meta:
        model = NewsModel
        fields = ['title', 'image']
