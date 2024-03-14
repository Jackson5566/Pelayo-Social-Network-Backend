from django.urls import path
from .views import NewspaperDetailView, CreateNewspaperView

urlpatterns = [
    path('newspaper_section/<int:id>', NewspaperDetailView.as_view(), name='newspaper'),
    path('newspaper_section/', CreateNewspaperView.as_view(), name='newspaper'),
]