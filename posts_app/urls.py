from django.urls import path
from .generics_view import PostsView, SearchPost, AllContentListView
from .views import PreSearch, PostView, GetCategoriesView, DeleteFileView, ContentListView


urlpatterns = [
    path('<int:_id>/', PostView.as_view()),
    path('', PostView.as_view()),
    path('pre-search', PreSearch.as_view()),
    path('get-categories/', GetCategoriesView.as_view()),
    path('allposts/', PostsView.as_view(), name='allposts'),
    path('delete-file/<int:id>/', DeleteFileView.as_view()),
    path('search/', SearchPost.as_view()),
    path('content_list/', ContentListView.as_view()),
    path('content_list/<int:content_list_id>/', ContentListView.as_view()),
    path('allcontent_list/', AllContentListView.as_view())
    # path('download/<int:pk>/', DownloadFileView.as_view(), name='download_file'),
]