from rest_framework import serializers
from .models import CategoryModel, PostModel, FileModel
from users_app.serializer import UsersSerializerReturn2
from api.serializers import BaseReturnSerializer, CategorySerializer
from message_app.serializer import MessageSerializer
from django.core.paginator import Paginator


class FilesSerializer(serializers.ModelSerializer):
    files = serializers.ListField(child=serializers.FileField())

    class Meta:
        model = FileModel
        fields = ['files']

    def create(self, validated_data):
        archivos = validated_data.pop('files')
        instances = []
        for archivo in archivos:
            file = FileModel.objects.create(files=archivo)
            instances.append(file)
        return instances


class PostsReturnSerializerWithUser(BaseReturnSerializer):
    user = UsersSerializerReturn2()


class PostsReturnSerializerWithoutUser(BaseReturnSerializer):
    pass


class PostsCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        exclude = ['user', 'likes', 'dislikes', 'files', 'messages', 'categories']

    def create(self, validated_data):
        instance = PostModel.objects.create(**validated_data, user=self.context['request'].user)
        return instance
