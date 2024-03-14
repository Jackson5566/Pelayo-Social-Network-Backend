
from django.urls import path
from .views import *

urlpatterns = [
  path('news/all', AllNewsView.as_view(), name='news'),
  path('news/<int:id>/', NewsDetailView.as_view(), name='news'),
  path('news/', CreateNewsView.as_view(), name='news'),
]