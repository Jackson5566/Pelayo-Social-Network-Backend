from .models import PostModel, CategoryModel, FileModel
from rest_framework import status, viewsets, generics
from rest_framework.response import Response
from .serializer import PostsReturnSerializerWithUser
from rest_framework.views import APIView
from .paginations import MyPagination
from api.serializers import CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from posts_app.classes.posts_classes.get_post import GetPostData
from .classes.like_proccessor import PostLikeProcessor
from .classes.search import SearchAlgorithm
from posts_app.classes.posts_classes.create_post import CreatePost
from .classes.posts_classes.update_post import UpdatePost
from .classes.posts_classes.delete_post import DeletePost
from api.shortcuts.data_get import process_and_get_response, process_and_get_queryset
from api.decorators.add_security import add_security


@add_security
class PostsView(APIView):
    def get(self, request, _id):
        context = {'request': request}
        get_post_data_instance = GetPostData(post_id=_id, request=request, context=context)
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


@add_security
class PostsViewSet(generics.ListAPIView):
    serializer_class = PostsReturnSerializerWithUser
    pagination_class = MyPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categories__name']

    def get_queryset(self):
        return PostModel.objects.all().order_by('-created')


@add_security
class SearchViewSet(viewsets.ModelViewSet):
    pagination_class = MyPagination
    serializer_class = PostsReturnSerializerWithUser

    def get_queryset(self):
        search_algorithm = SearchAlgorithm(request=self.request)
        return process_and_get_queryset(search_algorithm)


@add_security
class PreSearch(APIView):
    def get(self, request):
        title_posts = [post.title for post in PostModel.objects.all()]
        return Response(title_posts)


@add_security
class GetCategories(APIView):
    def get(self, request):
        categories = CategoryModel.objects.all()
        serialized_categories = CategorySerializer(categories, many=True)
        return Response(serialized_categories.data)


@add_security
class DeleteFile(APIView):
    def delete(self, request, post_id):
        try:
            file = FileModel.objects.get(id=post_id)
            file.delete()
            return Response({'message': 'Recurso eliminado con éxito'}, status=status.HTTP_200_OK)
        except FileModel.DoesNotExist:
            return Response({'message': 'Recurso no encontrado'}, status=status.HTTP_404_NOT_FOUND)

# @api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
# @authentication_classes([JWTAuthentication])
# def pre_search(request):
#     title_posts = [post.title for post in PostModel.objects.all()]
#     return Response(title_posts)


# @api_view(['GET'])
# @permission_classes([permissions.IsAuthenticated])
# @authentication_classes([JWTAuthentication])
# def get_categories(request):
# )

# @api_view(['DELETE'])
# @permission_classes([permissions.IsAuthenticated])
# @authentication_classes([JWTAuthentication])
# def delete_file(request, post_id):
#
#
