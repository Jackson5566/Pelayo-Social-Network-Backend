from rest_framework import serializers
from newspaper_app.models import NewspaperModel


class CreateNewspaperSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewspaperModel
        fields = ['title', 'image', 'text']


class GetNewspaperSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewspaperModel
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['image'] = instance.image.name
        return ret

