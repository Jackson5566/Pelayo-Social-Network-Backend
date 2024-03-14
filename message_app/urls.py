from django.urls import path
from .views import DetailMessageView, CommentsView, CreateMessageView

urlpatterns = [
  path('comment/<int:id>', DetailMessageView.as_view(), name='message'),
  path('comment/', CreateMessageView.as_view(), name='message'),
  path('comments/', CommentsView.as_view(), name='comments')
]