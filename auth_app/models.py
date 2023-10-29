from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(_("email address"), blank=False, unique=True, error_messages={
        "unique": "Un usuario con esa dirreción de correo electrónico ya existe.",
    }, )
    description = models.CharField(max_length=1000, blank=True, null=True, help_text=_('Descripcion del usuario'))
    denunciations = models.ManyToManyField('self', blank=True, help_text=_('Complaints imposed by other users'))
    isProfessor = models.BooleanField(default=False)

