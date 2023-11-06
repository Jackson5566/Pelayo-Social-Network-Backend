from rest_framework import status

from api.classes.controller_logic_excecutor import ResponseBody
from news_app.classes.bases.news_create_update_operations import NewsCreateUpdateOperations


class UpdateNewsOperation(NewsCreateUpdateOperations):
    """
    Nota: Llevar a la abstraccion estas operaciones comunes
    """
    def __init__(self, request):
        news_id = request.data.get('id')
        super().__init__(request=request, model_id=news_id)

    def create_or_update_process(self):
        self.update_news()
        self.response = ResponseBody(data={'message': 'Éxito con la actualización'}, status=status.HTTP_200_OK)

    def update_news(self):
        self.instance_manager.instance = self.serializer_manager.serializer.update(
            validated_data=self.serializer_manager.serializer.validated_data,
            instance=self.instance_manager.instance)
