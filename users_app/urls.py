from django.urls import path
from .views import SelectUserViewSet, CurrentUserInformation

urlpatterns = [
    path('user/<int:id>/', SelectUserViewSet.as_view()),
    path('current-user-information/', CurrentUserInformation.as_view())
]
