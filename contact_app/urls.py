from django.urls import path
from .views import SendMail

urlpatterns = [
    path('enviar-mail', SendMail.as_view())
]
