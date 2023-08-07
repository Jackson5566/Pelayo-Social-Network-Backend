from django.db import models
from PIL import Image
from api.settings import AUTH_USER_MODEL
from message_app.models import MessagesModel


class CategoryModel(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class FileModel(models.Model):
    files = models.FileField(upload_to='files')

    def __str__(self):
        return self.files.name


class PostModel(models.Model):
    title = models.CharField(max_length=100)  # Campo para el titulo
    description = models.CharField(max_length=300)  # Campo para la descripción
    text = models.TextField()  # Campo para el texto
    image = models.ImageField(upload_to='gallery', blank=True, null=True)  # Campo para la imagen
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True,
                             related_name="posts")  # Campo para el usuario
    likes = models.ManyToManyField(AUTH_USER_MODEL, related_name='likes')
    dislikes = models.ManyToManyField(AUTH_USER_MODEL, related_name='disslikes')
    files = models.ManyToManyField(FileModel)
    messages = models.ManyToManyField(MessagesModel, related_name="messages", blank=True)
    categories = models.ManyToManyField(CategoryModel, blank=True, related_name='categories')
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        last_img_path = self.image.path
        super().save(*args, **kwargs)
        if self.image and last_img_path != self.image.path:
            image = Image.open(self.image.path)
            if image.mode == "RGBA":
                image = image.convert("RGB")

            imagen_redimensionada = image.resize((800, 600), Image.LANCZOS)
            imagen_redimensionada.save(self.image.path, "JPEG", quality=50, optimize=True)

    def __str__(self):
        return self.title
