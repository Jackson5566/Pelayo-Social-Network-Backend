from posts_app.paginations import MyPagination
from posts_app.serializer import PostsReturnSerializerWithUser


def get_posts(cls):
    """
    Añade los atributos necesarios a las vistas para la obtención de posts
    """
    setattr(cls, 'serializer_class', PostsReturnSerializerWithUser)
    setattr(cls, 'pagination_class', MyPagination)
    return cls
