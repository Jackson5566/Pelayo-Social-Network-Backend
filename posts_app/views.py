from .models import PostModel, CategoryModel, FileModel
from rest_framework import status, permissions, viewsets, generics
from rest_framework.response import Response
from .serializer import PostsReturnSerializerWithUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
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


class PostsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, _id):
        post_instance = PostModel.objects.get(id=_id)
        context = {'request': request}
        get_post_data_instance = GetPostData(post_instance=post_instance, request=request, context=context)
        get_post_data_instance.start_process()
        return get_post_data_instance.response

    def post(self, request):
        create_post_instance = CreatePost(request=request)
        create_post_instance.start_process()
        return create_post_instance.response

    def delete(self, request, _id):
        post = PostModel.objects.get(id=_id)
        delete_post_instance = DeletePost(request=request, post_instance=post)
        delete_post_instance.start_process()
        return delete_post_instance.response

    def put(self, request):
        update_post_instance = UpdatePost(request=request)
        update_post_instance.start_process()
        return update_post_instance.response

    def patch(self, request, _id):
        post = PostModel.objects.get(id=_id)
        like_processor = PostLikeProcessor(request=request, post_instance=post)
        like_processor.start_process()
        return like_processor.response


class PostsViewSet(generics.ListAPIView):
    serializer_class = PostsReturnSerializerWithUser
    pagination_class = MyPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categories__name']

    def get_queryset(self):
        return PostModel.objects.all().order_by('-created')


class SearchViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    pagination_class = MyPagination
    serializer_class = PostsReturnSerializerWithUser

    def get_queryset(self):
        search_algorithm = SearchAlgorithm(request=self.request)
        search_algorithm.start_process()
        return search_algorithm.queryset


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def pre_search(request):
    title_posts = [post.title for post in PostModel.objects.all()]
    return Response(title_posts)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def get_categories(request):
    categories = CategoryModel.objects.all()
    serialized_categories = CategorySerializer(categories, many=True)
    return Response(serialized_categories.data)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
@authentication_classes([JWTAuthentication])
def delete_file(request, post_id):
    try:
        file = FileModel.objects.get(id=post_id)
        file.delete()
        return Response({'message': 'Recurso eliminado con éxito'}, status=status.HTTP_200_OK)
    except FileModel.DoesNotExist:
        return Response({'message': 'Recurso no encontrado'}, status=status.HTTP_404_NOT_FOUND)
