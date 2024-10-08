from rest_framework import status

from api.classes.controller_logic_excecutor import ResponseBody
from newspaper_app.classes.bases.newspaper_create_update_operations import NewspaperCreateUpdateOperations


class UpdateNewspaperOperation(NewspaperCreateUpdateOperations):
    """
    Nota: Llevar a la abstraccion estas operaciones comunes
    """
    def __init__(self, request, id):
        super().__init__(request=request, model_id=id)

    def create_or_update_process(self):
        self.update_news()
        self.response = ResponseBody(data={'message': 'Éxito con la actualización'}, status=status.HTTP_200_OK)

    def update_news(self):
        authenticated_user = self.request_manager.request.user
        if self.is_model_instance_from_user(user=authenticated_user):
            self.instance_manager.instance = self.serializer_manager.serializer.update(
                validated_data=self.serializer_manager.serializer.validated_data,
                instance=self.instance_manager.instance)
