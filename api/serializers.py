import os
from posts_app.models import PostModel, MessagesModel, CategoryModel
from rest_framework import serializers
from api.settings import BACKEND_URL

class CommentBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessagesModel
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['user'] = {
            'username': instance.user.username,
            'id': instance.user.id
        }
        return ret


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = '__all__'


class DynamicModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class BaseReturnSerializer(DynamicModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = PostModel
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['likes'] = instance.likes.count()
        ret['disslikes'] = instance.dislikes.count()
        ret['image'] = os.path.basename(instance.image.url) if instance.image else None
        ret['files'] = [
            {'url': BACKEND_URL + file.files.url, 'title': os.path.basename(file.files.name), 'id': file.id}
            for file in instance.files.all()]
        return ret
