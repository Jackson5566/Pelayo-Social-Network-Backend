from django.urls import path
from .views import PasswordChangeRequestView, PasswordChangeConfirmView, CreateUser, UsersView, denunciate, \
    CreateUserConfirmation
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'users', UsersView, basename="users")

urlpatterns = [
    path('change/password/', PasswordChangeRequestView.as_view()),
    path('change/password/confirm/<str:token>/', PasswordChangeConfirmView.as_view()),
    path('create-user', CreateUser.as_view()),
    path('create-user/confirmation/<str:token>/', CreateUserConfirmation.as_view()),
    path('denunciate/', denunciate)
]

urlpatterns += router.urls
