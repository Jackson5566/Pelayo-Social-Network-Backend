from django.db import models
from django.utils import timezone

# Create your models here.

class NewsModel(models.Model):
    title = models.CharField(max_length=60, error_messages={
        'max_length': 'Límite de texto excedido'
    }, help_text="Titulo de la noticia")
    image = models.ImageField(upload_to='news', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)