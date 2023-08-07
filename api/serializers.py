import os
from posts_app.models import PostModel, MessagesModel, CategoryModel
from rest_framework import serializers
from django.core.paginator import Paginator


class MessageBaseSerializer(serializers.ModelSerializer):
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
        # Don't pass the 'fields' arg up to the superclass
        fields = kwargs.pop('fields', None)

        # Instantiate the superclass normally
        super().__init__(*args, **kwargs)

        if fields is not None:
            # Drop any fields that are not specified in the `fields` argument.
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
            base_url = "https://pelayosn.up.railway.app"
            ret['likes'] = instance.likes.count()
            ret['disslikes'] = instance.dislikes.count()
            ret['image'] = base_url + instance.image.url if instance.image else None
            ret['files'] = [
                {'url': base_url + file.files.url, 'title': os.path.basename(file.files.name), 'id': file.id} for file
                in instance.files.all()]
            ret['messagesCount'] = instance.messages.count()
        return ret

    def serializer_posts(self, obj):
        if self.context['request'].query_params.get('edit') != 'true':
            page = self.context['request'].query_params.get('messagePage') or 1
            paginator = Paginator(obj.messages.all(), 4)
            to_serializer = paginator.page(page)
            to_serializer = MessageBaseSerializer(to_serializer, many=True)
            return to_serializer.data
