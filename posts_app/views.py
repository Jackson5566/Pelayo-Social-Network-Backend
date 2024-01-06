from django.db.models import Count

from .classes.posts_classes.add_to_content_list import AddToContentList
from .classes.posts_classes.create_content_list import CreateContentList
from .classes.posts_classes.delete_content_list import DeleteContentList
from .classes.posts_classes.g_posts_fl import GetPostsFL
from .models import PostModel, ContentListModel
from rest_framework.generics import ListAPIView
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
from .serializer import GetContentListSerializer


# Emplearme mas a fondo con temas de optimizacion
# Dividir esto en varias vistas para eliminar la incoherencia

@get_posts
@access_protected
class PostsView(ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categories__name', 'user__id', 'contents_list__name', 'contents_list__id']
    # Intentar ORdering de DRF

    def get_queryset(self):
        # Pensar si hace falta una optimizacion
        top = self.request.query_params.get('top')
        if top:
            pubs = PostModel.objects.annotate(num_likes=Count("likes")).select_related('user').prefetch_related('categories', 'files', 'likes',
                                                                                         'dislikes',
                                                                                         'messages', 'contents_list').order_by("-num_likes")[:top]
            return pubs
        return PostModel.objects.select_related('user').prefetch_related('categories', 'files', 'likes',
                                                                                         'dislikes',
                                                                                         'messages', 'contents_list').all().order_by(
            '-created')


@access_protected
class AllContentListView(ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user__id']
    serializer_class = GetContentListSerializer

    def get_queryset(self):
        return ContentListModel.objects.select_related('user').all().order_by('-created')


@access_protected
class ContentListView(APIView):

    def patch(self, request, content_list_id):
        added_instance = AddToContentList(request=request, content_list_id=content_list_id)
        return process_and_get_response(added_instance)

    def get(self, request, content_list_id):
        getter_instance = GetPostsFL(request=request, content_list_id=content_list_id)
        return process_and_get_response(getter_instance)

    def post(self, request):
        creation_instance = CreateContentList(request=request)
        return process_and_get_response(creation_instance)

    def delete(self, request, id):
        deletion_instance = DeleteContentList(request, content_list_id=id)
        return process_and_get_response(deletion_instance)


@get_posts
@access_protected
class SearchPost(ListAPIView):
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
        user_id = request.query_params.get('user_id')
        title_posts = PostModel.objects
        if user_id:
            title_posts = title_posts.filter(user__id=user_id)

        title_posts = title_posts.values_list('title', flat=True)
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
        return process_and_get_response(delete_file)

# @get_posts
# @access_protected
# class GetContentListView(ListAPIView):
#     filter_backends = [DjangoFilterBackend]
#     filterset_fields = ['categories__name', 'user__id']
#
#     def get_queryset(self):
#         return PostModel.objects.select_related('user', 'content_list').prefetch_related('categories', 'files', 'likes',
#                                                                                          'dislikes',
#                                                                                          'messages').all().order_by(
#             '-created')
