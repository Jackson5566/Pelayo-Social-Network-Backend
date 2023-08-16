from abc import ABC
from typing import Union
from posts_app.models import CategoryModel
from api.classes.serializer_manager import SerializerManager
from api.decorators.validate_serializer import validate_serializer
from api.classes.create_update_proccesor import CreateUpdateProcessor
from posts_app.serializer import FilesSerializer, PostsCreateSerializer
from posts_app.classes.posts_classes.bases.post_operations import PostOperations


class PostCreateUpdateOperations(PostOperations, CreateUpdateProcessor, ABC):
    def __init__(self, request, model_id=None):
        super().__init__(request=request, model_id=model_id)
        post_serializer = self._get_serializer_post()
        self.serializer_manager = SerializerManager(serializer=post_serializer)

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
                self.model_instance_manager.instance.categories.add(category_instance)

    def create_files(self) -> Union[None, list]:
        file_serializer = self.files_serializer()

        if file_serializer.is_valid():
            return file_serializer.create(validated_data=file_serializer.validated_data)# OJO devuelve una lista de ins

    def files_serializer(self):
        return FilesSerializer(data=self.request_manager.request.data)

    def add_files(self, files_instances):
        if files_instances:
            for file in files_instances:
                self.model_instance_manager.instance.files.add(file)
