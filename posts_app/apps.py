from django.apps import AppConfig
from django.db.models.signals import pre_delete


class PostsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts_app'

    def ready(self):
        from .signals import posts_callback
        from posts_app.models import PostModel

        pre_delete.connect(posts_callback, sender=PostModel)
