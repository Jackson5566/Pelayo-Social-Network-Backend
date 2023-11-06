from django.urls import path
from .views import NewspaperView

urlpatterns = [
    path('newspaper_section/<int:id>/', NewspaperView.as_view(), name='newspaper'),
    path('newspaper_section/', NewspaperView.as_view(), name='newspaper'),
]