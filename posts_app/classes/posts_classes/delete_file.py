from rest_framework import status
from posts_app.classes.posts_classes.bases.file_operations import FileOperations
from api.classes.controller_logic_excecutor import ResponseBody


class DeleteFile(FileOperations):
    def __init__(self, request, file_id):
        super().__init__(request=request, model_id=file_id)

    def start_process(self):
        self.instance_manager.instance.delete()
        self.response = ResponseBody(data={'message': 'Recurso eliminado con éxito'}, status=status.HTTP_200_OK)
