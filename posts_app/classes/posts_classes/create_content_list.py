from rest_framework import status

from api.classes.controller_logic_excecutor import ResponseBody
from posts_app.classes.posts_classes.bases.content_create_update_operations import ContentListCrUpOpr


class CreateContentList(ContentListCrUpOpr):

    def __init__(self, request):
        super().__init__(request=request)

    def create_or_update_process(self) -> None:
        self.create_post()
        self.response = ResponseBody(data={'message': 'Exito con la creación'}, status=status.HTTP_201_CREATED)

    def create_post(self):
        self.instance_manager.instance = self.serializer_manager.serializer.create(
            validated_data=self.serializer_manager.serializer.validated_data)
