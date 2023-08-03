from django.urls import path
from .views import MessageView

urlpatterns = [
  path('<int:id>/', MessageView.as_view()),
  path('', MessageView.as_view())
]