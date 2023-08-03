from django.contrib import admin
from .models import PostModel, FileModel, MessagesModel, CategoryModel

admin.site.register(PostModel)
admin.site.register(FileModel)
admin.site.register(MessagesModel)
admin.site.register(CategoryModel)
