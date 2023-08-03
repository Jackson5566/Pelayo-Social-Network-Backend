from django.urls import path
from .views import fsend_mail

urlpatterns = [
    path('enviar-mail', fsend_mail)
]
