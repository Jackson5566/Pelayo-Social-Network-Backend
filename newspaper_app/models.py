from django.db import models


# Create your models here.

class NewspaperModel(models.Model):
    title = models.CharField(max_length=100)
    img = models.ImageField(blank=True, null=True, upload_to='newspaper')
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.title