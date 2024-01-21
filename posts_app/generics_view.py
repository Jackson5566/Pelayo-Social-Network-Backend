from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from api.decorators.add_security import access_protected
from api.shortcuts.data_get import process_and_get_queryset
from posts_app.classes.search import SearchAlgorithm
from posts_app.models import PostModel, ContentListModel
from posts_app.serializer import GetContentListSerializer
from api.decorators.get_posts import get_posts


@get_posts
class PostsView(ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['categories__name', 'user__id', 'contents_list__name', 'contents_list__id']

    # Intentar ORdering de DRF

    def get_queryset(self):
        # Pensar si hace falta una optimizacion
        top = self.request.query_params.get('top')
        if top:
            pubs = PostModel.objects.annotate(num_likes=Count("likes")).select_related('user').prefetch_related(
                'categories', 'files', 'likes',
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


@get_posts
@access_protected
class SearchPost(ListAPIView):
    def get_queryset(self):
        search_algorithm = SearchAlgorithm(request=self.request)
        return process_and_get_queryset(search_algorithm)
