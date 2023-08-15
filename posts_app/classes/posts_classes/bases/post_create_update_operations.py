from abc import ABC, abstractmethod
from rest_framework import status
from api.classes.controller_logic_excecutor import ResponseBody
from api.decorators.validate_serializer import validate_serializer
from posts_app.classes.posts_classes.bases.post_operations import PostOperations
from posts_app.models import CategoryModel
from posts_app.serializer import FilesSerializer, PostsCreateSerializer
from typing import Union
from api.classes.create_update_proccesor import CreateUpdateProcessor
from api.classes.serializer_manager import SerializerManager


# Usar decoradores
class PostCreateUpdateOperations(PostOperations, CreateUpdateProcessor, ABC):
    def __init__(self, request):
        super().__init__(request=request)
        post_serializer = self._get_serializer_post()
        self.post_serializer_manager = SerializerManager(serializer=post_serializer)

    @validate_serializer('post_serializer_manager')
    def start_process(self):
        self.create_or_update_process()

    def _get_serializer_post(self):
        return PostsCreateSerializer(data=self.request_manager.request.data,
                                     context={'request': self.request_manager.request})

    def set_categories(self) -> None:
        for category in self.request_manager.request.data.getlist('categories'):
            category_instance = CategoryModel.objects.filter(name=category).first()
            if category_instance:
                self.post_instance_manager.instance.categories.add(category_instance)

    def create_files(self) -> Union[None, list]:
        file_serializer = self.files_serializer()

        if file_serializer.is_valid():
            return file_serializer.create(validated_data=file_serializer.validated_data)  # OJO Devuelve una lista

    def files_serializer(self):
        return FilesSerializer(data=self.request_manager.request.data)

    def add_files(self, files_instances):
        if files_instances:
            for file in files_instances:
                self.post_instance_manager.instance.files.add(file)
