from django.urls import path
from .views import MessageView

urlpatterns = [
  path('<int:id>/', MessageView.as_view(), name='message'),
  path('', MessageView.as_view(), name='message')
]