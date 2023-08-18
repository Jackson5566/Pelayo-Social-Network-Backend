from api.serializers import CategorySerializer
from api.classes.serialzer_operations import SerializerOperations
from api.classes.controller_logic_excecutor import ControllerLogicExecutor, ResponseBody
from posts_app.models import CategoryModel
from rest_framework import status


class GetCategories(ControllerLogicExecutor, SerializerOperations):
    def __init__(self, request):
        ControllerLogicExecutor.__init__(self, request=request)
        SerializerOperations.__init__(self)

    def _get_serializer(self, **kwargs):
        queryset = CategoryModel.objects.all()
        return CategorySerializer(queryset, many=True)

    def start_process(self):
        self.response = ResponseBody(data=self.serializer_manager.serializer.data, status=status.HTTP_200_OK)
