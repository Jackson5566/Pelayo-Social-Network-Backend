from .classes.posts_classes.add_to_content_list import AddToContentList
from .classes.posts_classes.create_content_list import CreateContentList
from .classes.posts_classes.delete_content_list import DeleteContentList
from .classes.posts_classes.g_posts_fl import GetPostsFL
from rest_framework.response import Response
from rest_framework.views import APIView
from posts_app.classes.posts_classes.get_post import GetPostData
from .classes.like_proccessor import PostLikeProcessor
from posts_app.classes.posts_classes.create_post import CreatePost
from .classes.posts_classes.update_post import UpdatePost
from .classes.posts_classes.delete_post import DeletePost
from api.shortcuts.data_get import process_and_get_response
from api.decorators.add_security import access_protected
from posts_app.classes.posts_classes.delete_file import DeleteFile
from posts_app.classes.posts_classes.get_categories import GetCategories
from drf_spectacular.utils import extend_schema
from .serializer import *


@access_protected
class CreateContentListView(APIView):
    @extend_schema(
        responses={200: str, 404: str},
    )
    def post(self, request):
        creation_instance = CreateContentList(request=request)
        return process_and_get_response(creation_instance)


class ContentListDetailView(APIView):
    @extend_schema(
        responses={200: str, 404: str},
    )
    def patch(self, request, content_list_id):
        added_instance = AddToContentList(request=request, content_list_id=content_list_id)
        return process_and_get_response(added_instance)

    def get(self, request, content_list_id):
        getter_instance = GetPostsFL(request=request, content_list_id=content_list_id)
        return process_and_get_response(getter_instance)

    @extend_schema(
        responses={200: str, 404: str},
    )
    def delete(self, request, content_list_id):
        deletion_instance = DeleteContentList(request, content_list_id=content_list_id)
        return process_and_get_response(deletion_instance)


@access_protected
class PostDetailView(APIView):
    @extend_schema(
        responses={200: PostsReturnSerializerWithoutUser, 404: str},
    )
    def get(self, request, _id):
        get_post_data_instance = GetPostData(post_id=_id, request=request)
        return process_and_get_response(get_post_data_instance)

    @extend_schema(
        responses={200: str, 404: str},
    )
    def delete(self, request, _id):
        delete_post_instance = DeletePost(request=request, post_id=_id)
        return process_and_get_response(delete_post_instance)

    @extend_schema(
        responses={200: str, 404: str},
    )
    # Añadir id
    def put(self, request, _id):
        update_post_instance = UpdatePost(request=request, post_id=_id)
        return process_and_get_response(update_post_instance)


class CreatePostView(APIView):
    @extend_schema(
        responses={200: str, 404: str},
    )
    def post(self, request):
        create_post_instance = CreatePost(request=request)
        return process_and_get_response(create_post_instance)


class LikePostView(APIView):
    @extend_schema(
        responses={200: str, 404: str},
    )
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
    @extend_schema(
        responses={200: str, 404: list[str]},
    )
    def get(self, request):
        get_categories = GetCategories(request=request)
        return process_and_get_response(get_categories)


@access_protected
class DeleteFileView(APIView):
    @extend_schema(
        responses={200: str, 404: str},
    )
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
