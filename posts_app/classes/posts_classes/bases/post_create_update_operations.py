from abc import ABC, abstractmethod
from posts_app.classes.posts_classes.bases.post_operations import PostOperations
from posts_app.models import CategoryModel
from posts_app.serializer import FilesSerializer
from typing import Union


class PostCreateUpdateOperations(PostOperations, ABC):
    def __init__(self, request):
        super().__init__(post_instance=None, request=request)
        self.post_serializer = self._get_serializer_post()

    def __str__(self):
        print(
            f"""
            Instancia del post: {self.post_instance} \n
            Serializer del post: {self.post_serializer}
            """
        )

    @abstractmethod
    def _get_serializer_post(self):
        pass

    def set_categories(self) -> None:
        for category in self.request_manager.request.data.getlist('categories'):
            category_instance = CategoryModel.objects.filter(name=category).first()
            if category_instance:
                self.post_instance.categories.add(category_instance)

    def create_files(self) -> Union[None, list]:
        file_serializer = self.files_serializer()

        if file_serializer.is_valid():
            return file_serializer.create(validated_data=file_serializer.validated_data)  # OJO Devuelve una lista

    def files_serializer(self):
        return FilesSerializer(data=self.request_manager.request.data)

    def add_files(self, files_instances):
        if files_instances:
            for file in files_instances:
                self.post_instance.files.add(file)
