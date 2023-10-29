from django.urls import path
from .views import MessageView, CommentsView

urlpatterns = [
  path('message/<int:id>/', MessageView.as_view(), name='message'),
  path('message/', MessageView.as_view(), name='message'),
  path('messages/', CommentsView.as_view(), name='comments')
]