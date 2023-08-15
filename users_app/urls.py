from django.urls import path, include
from .views import SelectUserViewSet, SelectCurrentlyUserViewSet, CurrentInformation
from rest_framework import routers

router = routers.DefaultRouter()
# router.register(r'usersview', SelectUserViewSet, basename="usersview")
router.register(r'user', SelectUserViewSet, basename="user")
# router.register(r'user-config', SelectCurrentlyUserViewSet, basename="user-config")

urlpatterns = [
    # path('user-config', user_config)
    path('user-config/', SelectCurrentlyUserViewSet.as_view()),
    path('current-user-information/', CurrentInformation.as_view())
]
urlpatterns += router.urls