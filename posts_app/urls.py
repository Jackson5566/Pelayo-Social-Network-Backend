from django.urls import path
from .views import PreSearch, PostsView, PostsViewSet, SearchViewSet, GetCategories, DeleteFile
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'search', SearchViewSet, basename='search')


urlpatterns = [
    path('<int:_id>/', PostsView.as_view()),
    path('', PostsView.as_view()),
    path('pre-search', PreSearch.as_view()),
    path('get-categories/', GetCategories.as_view()),
    path('allposts/', PostsViewSet.as_view(), name='allposts'),
    path('delete-file/<int:id>/', DeleteFile.as_view())
]

urlpatterns += router.urls