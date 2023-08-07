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
        # Se llama al original de la clase Model
        print(f'{args}')
        print(f'{kwargs}')
        print(kwargs['image'])

        super().save(*args, **kwargs)
        # Se captura la imagen guardada
        if self.image:
            imagen = Image.open(self.image.path)
            # Si el modo de la imagen es RGBA se transforma en RGB
            if imagen.mode == "RGBA":
                imagen = imagen.convert("RGB")
            # Se redimensiona la imagen y se le añade un suavizado
            imagen_redimensionada = imagen.resize((800, 600), Image.LANCZOS)
            # Se guarda la imagen
            imagen_redimensionada.save(self.image.path, "JPEG", quality=50, optimize=True)

    def __str__(self):
        return self.title
