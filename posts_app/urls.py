from django.urls import path
from .views import PreSearch, PostView, PostsView, SearchPost, GetCategories, DeleteFile
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'search', SearchPost, basename='search')


urlpatterns = [
    path('<int:_id>/', PostView.as_view()),
    path('', PostView.as_view()),
    path('pre-search', PreSearch.as_view()),
    path('get-categories/', GetCategories.as_view()),
    path('allposts/', PostsView.as_view(), name='allposts'),
    path('delete-file/<int:id>/', DeleteFile.as_view())
]

urlpatterns += router.urls