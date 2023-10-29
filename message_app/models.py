from django.db import models
from api.settings import AUTH_USER_MODEL


class MessagesModel(models.Model):
    content = models.CharField(max_length=10000, error_messages={
        'max_length': 'El límite de texto impuesto es de 10000 caracteres, no puede exceder'
    })
    user = models.ForeignKey(AUTH_USER_MODEL, blank=True, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"created by: {self.user.username}, id{self.id}"
