from rest_framework import status

from api.classes.controller_logic_excecutor import ResponseBody
from api.classes.type_alias.operations import DeleteProcessor
from news_app.classes.bases.newsOperations import NewsOperations


class DeleteNewsOperation(NewsOperations, DeleteProcessor):
    def __init__(self, request, news_id):
        NewsOperations.__init__(self, request=request, model_id=news_id)
        DeleteProcessor.__init__(self)

    def start_process(self):
        self.delete()
        self.response = ResponseBody(data={'message': 'Recurso eliminado con éxito'}, status=status.HTTP_200_OK)

    def delete(self):
        self.instance_manager.instance.delete()
