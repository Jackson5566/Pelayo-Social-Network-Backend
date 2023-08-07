from .models import PostModel, CategoryModel, FileModel
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from .serializer import PostsReturnSerializerWithUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.views import APIView
from .paginations import MyPagination
from api.serializers import CategorySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from posts_app.classes.posts_classes.get_post import GetPostData
from .classes.like_proccessor import PostLikeProcessor
from .classes.search import SearchAlgorithm
from rest_framework.exceptions import ValidationError
from posts_app.classes.posts_classes.create_post import CreatePost
from .classes.posts_classes.update_post import UpdatePost, NotAllowed


class PostsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, _id):
        post_instance = PostModel.objects.get(id=_id)
        context = {'request': request}
        get_post_data_instance = GetPostData(post_instance=post_instance, request=request, context=context)
        return Response(get_post_data_instance.get_post_data())

    def post(self, request: object):
        create_post_instance = CreatePost(request=request)
        try:
            create_post_instance.create_post()
            return Response({'message': 'Exito con la creación'}, status=status.HTTP_201_CREATED)

        except ValidationError as err:
            return Response({'message': str(err)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, _id):
        post = PostModel.objects.get(id=_id)
        post.delete()
        return Response({'message': 'Delete'}, status=status.HTTP_200_OK)

    def put(self, request):
        update_post_instance = UpdatePost(request=request)
        try:
            update_post_instance.start_update_post()
        except ValueError as error:
            return Response({
                'message': str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        except NotAllowed as error:
            return Response({
                'message': str(error)
            }, status=status.HTTP_403_FORBIDDEN)

    def patch(self, request, _id):
        like_processor = PostLikeProcessor(request=request, post_id=_id)
        like_processor.start_process()

        return Response({
            "likes": like_processor.likes,
            "disslikes": like_processor.dislikes
        }, status=status.HTTP_200_OK)


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
        search_algorithm = SearchAlgorithm(search=self.request.query_params.get('search'))
        search_algorithm.start_search()
        return search_algorithm.get_searched_posts()


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
