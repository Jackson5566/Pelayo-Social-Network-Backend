from django.urls import path, include
from .views import SelectUserViewSet, SelectCurrentlyUserViewSet, CurrentUserInformation
from rest_framework import routers

# router = routers.DefaultRouter()
# # router.register(r'usersview', SelectUserViewSet, basename="usersview")
# # router.register(r'user', SelectUserViewSet, basename="user")
# # router.register(r'user-config', SelectCurrentlyUserViewSet, basename="user-config")

urlpatterns = [
    # path('user-config', user_config)
    path('user/<int:id>/', SelectUserViewSet.as_view()),
    path('user-config/', SelectCurrentlyUserViewSet.as_view()),
    path('current-user-information/', CurrentUserInformation.as_view())
]
# urlpatterns += router.urls