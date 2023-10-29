from rest_framework import status
from api.classes.controller_logic_excecutor import ResponseBody
from newspaper_app.classes.bases.newspaper_create_update_operations import NewspaperCreateUpdateOperations


class CreateNewspaperOperation(NewspaperCreateUpdateOperations):
    def __init__(self, request):
        super().__init__(request=request)

    def create_or_update_process(self):
        self.create_news()
        self.response = ResponseBody(data={'message': 'Exito con la creación'}, status=status.HTTP_200_OK)

    def create_news(self):
        self.instance_manager.instance = self.serializer_manager.serializer.create(
            validated_data=self.serializer_manager.serializer.validated_data)
