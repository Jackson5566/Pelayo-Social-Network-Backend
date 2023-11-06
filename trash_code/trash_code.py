# from rest_framework import serializers
# from .models import FileModel
#
# class FileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FileModel
#         fields = '__all__'
#         read_only_fields = ('files',)
#
# from rest_framework.generics import RetrieveAPIView
# from django.http import FileResponse
#
# class DownloadFileView(RetrieveAPIView):
#     queryset = FileModel.objects.all()
#     serializer_class = FileSerializer
#     lookup_field = 'pk'
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         file = instance.files
#
#         response = FileResponse(file, as_attachment=True)
#
#         return response
#
