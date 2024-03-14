from django.urls import path
from .generics_view import PostsView, SearchPost, AllContentListView
from .views import *



urlpatterns = [
    path('like/<int:_id>', LikePostView.as_view()),
    path('<int:_id>/', PostDetailView.as_view()),
    path('', CreatePostView.as_view()),
    path('pre-search', PreSearch.as_view()),
    path('get-categories/', GetCategoriesView.as_view()),
    path('allposts/', PostsView.as_view(), name='allposts'),
    path('delete-file/<int:id>/', DeleteFileView.as_view()),
    path('search/', SearchPost.as_view()),
    path('content_list/', CreateContentListView.as_view()),
    path('content_list/<int:content_list_id>', ContentListDetailView.as_view()),
    path('allcontent_list/', AllContentListView.as_view())
    # path('download/<int:pk>/', DownloadFileView.as_view(), name='download_file'),
]