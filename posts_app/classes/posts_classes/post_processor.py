from posts_app.models import CategoryModel
from posts_app.serializer import FilesSerializer


class PostCreateUpdateProcessor:
    @staticmethod
    def set_categories(post_instance, request) -> None:
        for category in request.data.getlist('categories'):
            category_instance = CategoryModel.objects.filter(name=category).first()
            if category_instance:
                post_instance.categories.add(category_instance)

    @staticmethod
    def serialize_files(request):
        file_serializer = FilesSerializer(data=request.data)

        if file_serializer.is_valid():
            files_instances = file_serializer.create(validated_data=file_serializer.validated_data)
        else:
            files_instances = None

        return files_instances

    @staticmethod
    def add_files(files_instances, post_instance):
        if files_instances:
            for file in files_instances:
                post_instance.files.add(file)

    @staticmethod
    def is_from_authenticated_user(user, post_instance) -> bool:
        return user == post_instance

# Arreglar los parametros de los metodos estaticos