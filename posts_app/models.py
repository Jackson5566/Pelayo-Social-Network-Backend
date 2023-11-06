from django.db import models
from PIL import Image
from api.settings import AUTH_USER_MODEL
from message_app.models import MessagesModel


# Filosofia: Los usuario podran meter datos en las listas de otros con una autorizacion

class CategoryModel(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class FileModel(models.Model):
    files = models.FileField(upload_to='files')

    def __str__(self):
        return self.files.name


class ContentListModel(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="content_list")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PostModel(models.Model):
    title = models.CharField(max_length=100)  # Campo para el titulo
    description = models.CharField(max_length=300)  # Campo para la descripción
    text = models.TextField()  # Campo para el texto
    image = models.ImageField(upload_to='gallery', blank=True, null=True)  # Campo para la imagen
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="posts")  # Campo para el usuario
    likes = models.ManyToManyField(AUTH_USER_MODEL, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(AUTH_USER_MODEL, related_name='disslikes', blank=True)
    files = models.ManyToManyField(FileModel, blank=True)
    messages = models.ManyToManyField(MessagesModel, related_name="messages", blank=True)
    categories = models.ManyToManyField(CategoryModel, blank=True, related_name='categories')
    content_list = models.ForeignKey(ContentListModel, blank=True, null=True, on_delete=models.CASCADE,
                                     related_name="posts", default=None)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        last_img_path = self.image.path if self.image else None
        super().save(*args, **kwargs)
        if self.image and last_img_path != self.image.path:
            image = Image.open(self.image.path)
            if image.mode == "RGBA":
                image = image.convert("RGB")

            resized_image = image.resize((800, 600), Image.LANCZOS)
            resized_image.save(self.image.path, "JPEG", quality=50, optimize=True)

    def __str__(self):
        return self.title
