from rest_framework import status

from posts_app.classes.posts_classes.bases.content_operations import ContentListOperations
from api.classes.controller_logic_excecutor import ResponseBody
from api.classes.type_alias.operations import DeleteProcessor


class DeleteContentList(ContentListOperations, DeleteProcessor):

    def __init__(self, request, content_list_id):
        super().__init__(request=request, model_id=content_list_id)

    def start_process(self):
        self.delete()
        self.response = ResponseBody(data={'message': 'Recurso eliminado con éxito'}, status=status.HTTP_200_OK)

    def delete(self):
        self.instance_manager.instance.delete()
