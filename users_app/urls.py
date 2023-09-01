from django.urls import path
from .views import SelectedUserInfo, CurrentUserInformation

urlpatterns = [
    path('user/<int:id>/', SelectedUserInfo.as_view()),
    path('current-user-information/', CurrentUserInformation.as_view())
]
