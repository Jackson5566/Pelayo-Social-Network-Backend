from django.urls import path
from .views import PreSearch, PostView, PostsView, SearchPost, GetCategoriesView, DeleteFileView, DownloadFileView

urlpatterns = [
    path('<int:_id>/', PostView.as_view()),
    path('', PostView.as_view()),
    path('pre-search', PreSearch.as_view()),
    path('get-categories/', GetCategoriesView.as_view()),
    path('allposts/', PostsView.as_view(), name='allposts'),
    path('delete-file/<int:id>/', DeleteFileView.as_view()),
    path('search/', SearchPost.as_view()),
    path('download/<int:pk>/', DownloadFileView.as_view(), name='download_file'),
]