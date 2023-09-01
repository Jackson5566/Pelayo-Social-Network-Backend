from rest_framework import status
from api.classes.controller_logic_excecutor import ResponseBody
from posts_app.classes.posts_classes.bases.post_operations import PostOperations


# Eliminar el innecesario id que se recibe como parametro en la vista, ademas optimizar el acceso a la base de datos

class PostLikeProcessor(PostOperations):
    def __init__(self, request, post_id):
        super().__init__(request=request, model_id=post_id)
        self.user_in_post_like = self.is_user_in_post_like()
        self.user_in_post_dislikes = self.is_user_in_post_dislikes()
        self.likes = int(self.get_likes())
        self.dislikes = int(self.get_dislikes())

    def is_user_in_post_like(self) -> bool:
        return self.request_manager.request.user in self.instance_manager.instance.likes.all()

    def is_user_in_post_dislikes(self) -> bool:
        return self.request_manager.request.user in self.instance_manager.instance.dislikes.all()

    def start_process(self) -> None:
        if self.user_did_like():
            self.decrease_likes() if self.user_in_post_like else self.increase_likes()
            if self.user_in_post_dislikes:
                self.decrease_dislikes()
        else:
            self.decrease_dislikes() if self.user_in_post_dislikes else self.increase_dislikes()
            if self.user_in_post_like:
                self.decrease_likes()

        self.response = ResponseBody(data={"likes": self.likes, "disslikes": self.dislikes}, status=status.HTTP_200_OK)

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
