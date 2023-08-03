from rest_framework import serializers
from auth_app.models import User
from api.serializers import BaseReturnSerializer
from django.core.paginator import Paginator
from api.serializers import DynamicModelSerializer

class UsersSerializerReturn(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField('serializer_posts')

    class Meta:
        model = User
        fields = ['email', 'username', 'last_name', 'id', 'posts']

    def serializer_posts(self, obj):
        if self.context['request'].query_params.get('onlyInformation') != 'true':
            page = self.context['request'].query_params.get('page') or 1
            paginator = Paginator(obj.posts.all(), 4)
            to_serializer = paginator.page(page)
            to_serializer = BaseReturnSerializer(to_serializer, many=True, context=self.context)
            return to_serializer.data
        return None
        
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if self.context['request'].query_params.get('onlyPosts') != 'true':
            ret['postsCount'] = len(instance.posts.all())
        return ret
    
class UsersSerializerReturn2(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'last_name', 'id']

class UsersLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password']

class UserInformationSerializer(DynamicModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'last_name']