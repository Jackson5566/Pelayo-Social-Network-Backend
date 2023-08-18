from posts_app.paginations import MyPagination
from posts_app.serializer import PostsReturnSerializerWithUser


def get_posts(cls):
    setattr(cls, 'serializer_class', PostsReturnSerializerWithUser)
    setattr(cls, 'pagination_class', MyPagination)
    return cls
