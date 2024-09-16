from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from api.customs.custom_storage import FirebaseStorage


class User(AbstractUser):
    user_photo = ProcessedImageField(upload_to='images/user',
                                     processors=[ResizeToFill(200, 200)],
                                     format='JPEG', options={'quality': 50},
                                     storage=FirebaseStorage(), blank=True, null=True)
    email = models.EmailField(_("email address"), blank=False, unique=True, error_messages={
        "unique": "Un usuario con esa dirreción de correo electrónico ya existe.",
    }, )
    description = models.CharField(max_length=1000, blank=True, null=True, help_text='Descripción del usuario')
    denunciations = models.ManyToManyField('self', blank=True, help_text='Complaints imposed by other users')
    points = models.IntegerField(default=50)
    isProfessor = models.BooleanField(default=False)
