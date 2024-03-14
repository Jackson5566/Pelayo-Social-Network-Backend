from django.db import models
from api.settings import AUTH_USER_MODEL
from message_app.models import MessagesModel
from api.customs.custom_storage import FirebaseStorage
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


# Filosofia: Los usuario podran meter datos en las listas de otros con una autorizacion


class CategoryModel(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class FileModel(models.Model):
    files = models.FileField(upload_to='files', storage=FirebaseStorage())

    def __str__(self):
        return self.files.name


class ContentListModel(models.Model):
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="contents_list")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class PostModel(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    text = models.TextField()
    image = ProcessedImageField(upload_to='images/gallery',
                                processors=[ResizeToFill(800, 600)],
                                format='JPEG', options={'quality': 60},
                                storage=FirebaseStorage(), blank=True, null=True)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name="posts")
    likes = models.ManyToManyField(AUTH_USER_MODEL, related_name='likes', blank=True)
    dislikes = models.ManyToManyField(AUTH_USER_MODEL, related_name='disslikes', blank=True)
    files = models.ManyToManyField(FileModel, blank=True)
    messages = models.ManyToManyField(MessagesModel, related_name="messages", blank=True)
    categories = models.ManyToManyField(CategoryModel, blank=True, related_name='categories')
    contents_list = models.ManyToManyField(ContentListModel, blank=True, null=True, related_name="posts", default=None)
    created = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(editable=False, default=00000000000)

    def __str__(self):
        return f"Post: {self.title}, De Usuario: {self.user.username}, Con ID: {self.id}"
