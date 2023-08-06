from ..models import PostModel


class PostLikeProcessor:
    def __init__(self, request, post_id):
        self.request = request
        self.post = PostModel.objects.get(id=post_id)
        self.user_in_post_like = self.is_user_in_post_like()
        self.user_in_post_dislikes = self.is_user_in_post_dislikes()
        self.likes = self.get_likes()
        self.dislikes = self.get_dislikes()

    def is_user_in_post_like(self) -> bool:
        return self.request.user in self.post.likes.all()

    def is_user_in_post_dislikes(self) -> bool:
        return self.request.user in self.post.disslikes.all()

    def start_process(self) -> None:
        if self.user_did_like():
            self.decrease_likes() if self.user_in_post_like else self.increase_likes()
        else:
            self.decrease_dislikes() if self.user_in_post_dislikes else self.increase_dislikes()

    def user_did_like(self) -> bool:
        if self.request.data['like']:
            return True
        return False

    def get_likes(self) -> int:
        return self.request.data['likes']

    def get_dislikes(self) -> int:
        return self.request.data['disslikes']

    def decrease_likes(self) -> None:
        self.post.likes.remove(self.request.user)
        self.likes -= 1

    def increase_likes(self) -> None:
        self.post.likes.add(self.request.user)
        self.likes += 1

    def decrease_dislikes(self) -> None:
        self.post.disslikes.remove(self.request.user)
        self.dislikes -= 1

    def increase_dislikes(self) -> None:
        self.post.disslikes.add(self.request.user)
        self.dislikes += 1
