from rest_framework import serializers


class ContactSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    content = serializers.CharField()
    subject = serializers.CharField()
