
from django.urls import path
from .views import NewsView, NewsProcessingView

urlpatterns = [
  path('news/<int:id>/', NewsView.as_view(), name='news'),
  path('news/edit/<int:id>/', NewsProcessingView.as_view(), name='news'),
  path('news', NewsView.as_view(), name='news'),
]