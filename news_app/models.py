from django.db import models
from api.customs.custom_storage import FirebaseStorage


class NewsModel(models.Model):
    title = models.CharField(max_length=100, error_messages={
        'max_length': 'Límite de texto excedido'
    }, help_text="Titulo de la noticia")
    image = models.ImageField(upload_to='images/news', blank=True, null=True, storage=FirebaseStorage())
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title
