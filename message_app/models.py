from django.db import models
# from django.contrib.auth.models import User

from api.settings import AUTH_USER_MODEL


class MessagesModel(models.Model):
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=150)
    user = models.ForeignKey(AUTH_USER_MODEL, blank=True, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.title}, created by: {self.user.username}"
