from rest_framework import status
from api.classes.controller_logic_excecutor import ResponseBody
from posts_app.classes.posts_classes.bases.post_operations import PostOperations
from django.core.exceptions import ObjectDoesNotExist


# Eliminar el innecesario id que se recibe como parametro en la vista, además optimizar el acceso a la base de datos

class PostLikeProcessor(PostOperations):
    def __init__(self, request, post_id):
        super().__init__(request=request, model_id=post_id)

        self.likes = int(self.get_likes())
        self.dislikes = int(self.get_dislikes())

    def is_user_in_post_like(self) -> bool:
        authenticated_user = self.request_manager.request.user
        try:
            user_in_post_like = self.instance_manager.instance.likes.get(id=authenticated_user.id)
        except ObjectDoesNotExist:
            user_in_post_like = None
        return True if user_in_post_like else False

    def is_user_in_post_dislikes(self) -> bool:
        authenticated_user = self.request_manager.request.user
        try:
            user_in_post_dislikes = self.instance_manager.instance.dislikes.get(id=authenticated_user.id)
        except ObjectDoesNotExist:
            user_in_post_dislikes = None

        return user_in_post_dislikes is not None

    def start_process(self) -> None:
        user_in_post_like = self.is_user_in_post_like()
        user_in_post_dislikes = self.is_user_in_post_dislikes()

        if self.user_did_like():
            self.decrease_likes() if user_in_post_like else self.increase_likes()
            if user_in_post_dislikes:
                self.decrease_dislikes()

        else:
            self.decrease_dislikes() if user_in_post_dislikes else self.increase_dislikes()
            if user_in_post_like:
                self.decrease_likes()

        self.response = ResponseBody(data={"likes": self.likes, "dislikes": self.dislikes}, status=status.HTTP_200_OK)

    def user_did_like(self) -> bool:
        if bool(self.request_manager.request.data.get('like')):
            return True
        return False

    def get_likes(self) -> int:
        return self.request_manager.request.data.get('likes')

    def get_dislikes(self) -> int:
        return self.request_manager.request.data.get('disslikes')

    def decrease_likes(self) -> None:
        self.instance_manager.instance.likes.remove(self.request_manager.request.user)
        self.likes -= 1

    def increase_likes(self) -> None:
        self.instance_manager.instance.likes.add(self.request_manager.request.user)
        self.likes += 1

    def decrease_dislikes(self) -> None:
        self.instance_manager.instance.dislikes.remove(self.request_manager.request.user)
        self.dislikes -= 1

    def increase_dislikes(self) -> None:
        self.instance_manager.instance.dislikes.add(self.request_manager.request.user)
        self.dislikes += 1
