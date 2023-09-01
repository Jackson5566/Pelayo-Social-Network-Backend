import os
from posts_app.models import PostModel, MessagesModel, CategoryModel
from rest_framework import serializers
from django.core.paginator import Paginator
from api.settings import BACKEND_URL

class CommentBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessagesModel
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['user'] = instance.user.username
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
    messages = serializers.SerializerMethodField('serializer_posts')
    categories = CategorySerializer(many=True)

    class Meta:
        model = PostModel
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if self.context['request'].query_params.get('onlyMessages') != 'true':
            ret['likes'] = instance.likes.count()
            ret['disslikes'] = instance.dislikes.count()
            ret['image'] = BACKEND_URL + instance.image.url if instance.image else None
            ret['files'] = [
                {'url': BACKEND_URL + file.files.url, 'title': os.path.basename(file.files.name), 'id': file.id}
                for file in instance.files.all()]
            ret['messagesCount'] = instance.messages.count()
        return ret

    def serializer_posts(self, obj):
        if self.context['request'].query_params.get('edit') != 'true':
            page = self.context['request'].query_params.get('messagePage') or 1
            messages = obj.messages.all().order_by('id')
            paginator = Paginator(messages, 4)
            to_serializer = paginator.page(page)
            to_serializer = CommentBaseSerializer(to_serializer, many=True)
            return to_serializer.data
