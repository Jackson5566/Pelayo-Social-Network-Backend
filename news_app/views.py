from rest_framework.views import APIView

from api.decorators.add_security import access_protected
from api.shortcuts.data_get import process_and_get_response
from news_app.classes.createNewsOperation import CreateNewsOperation
from news_app.classes.deleteNewsOperation import DeleteNewsOperation
from news_app.classes.getNewsOperation import GetNewsOperation
from news_app.classes.updateNewsOperation import UpdateNewsOperation
from news_app.models import NewsModel


# Create your views here.

@access_protected
class NewsView(APIView):
    def get(self, request):
        get_news_instance = GetNewsOperation(request=request, news_instance=NewsModel.objects.all())
        return process_and_get_response(get_news_instance)

    def post(self, request):
        create_news_instance = CreateNewsOperation(request=request)
        return process_and_get_response(create_news_instance)

    def put(self, request):
        update_news_instance = UpdateNewsOperation(request=request)
        return process_and_get_response(update_news_instance)

    def delete(self, request, id):
        delete_news_instance = DeleteNewsOperation(request=request, news_id=id)
        return process_and_get_response(delete_news_instance)

