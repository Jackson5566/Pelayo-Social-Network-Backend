from .models import PostModel
from rest_framework import viewsets, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from posts_app.classes.posts_classes.get_post import GetPostData
from .classes.like_proccessor import PostLikeProcessor
from .classes.search import SearchAlgorithm
from posts_app.classes.posts_classes.create_post import CreatePost
from .classes.posts_classes.update_post import UpdatePost
from .classes.posts_classes.delete_post import DeletePost
from api.shortcuts.data_get import process_and_get_response, process_and_get_queryset
from api.decorators.add_security import access_protected
from api.decorators.get_posts import get_posts
from posts_app.classes.posts_classes.delete_file import DeleteFile
from posts_app.classes.posts_classes.get_categories import GetCategories


# Emplearme mas a fondo con temas de optimizacion

@get_posts
@access_protected
class PostsView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categories__name']

    def get_queryset(self):
        return PostModel.objects.select_related('user').prefetch_related('categories', 'files', 'likes', 'dislikes',
                                                                         'messages').all().order_by('-created')


@get_posts
@access_protected
class SearchPost(viewsets.ModelViewSet):
    def get_queryset(self):
        search_algorithm = SearchAlgorithm(request=self.request)
        return process_and_get_queryset(search_algorithm)


@access_protected
class PostView(APIView):
    def get(self, request, _id):
        get_post_data_instance = GetPostData(post_id=_id, request=request)
        return process_and_get_response(get_post_data_instance)

    def post(self, request):
        create_post_instance = CreatePost(request=request)
        return process_and_get_response(create_post_instance)

    def delete(self, request, _id):
        delete_post_instance = DeletePost(request=request, post_id=_id)
        return process_and_get_response(delete_post_instance)

    def put(self, request):
        update_post_instance = UpdatePost(request=request)
        return process_and_get_response(update_post_instance)

    def patch(self, request, _id):
        like_processor = PostLikeProcessor(request=request, post_id=_id)
        return process_and_get_response(like_processor)


@access_protected
class PreSearch(APIView):
    def get(self, request):
        title_posts = PostModel.objects.values_list('title', flat=True)
        return Response(title_posts)


@access_protected
class GetCategoriesView(APIView):
    def get(self, request):
        get_categories = GetCategories(request=request)
        return process_and_get_response(get_categories)


@access_protected
class DeleteFileView(APIView):
    def delete(self, request, id):
        delete_file = DeleteFile(request=request, file_id=id)
        process_and_get_response(delete_file)
