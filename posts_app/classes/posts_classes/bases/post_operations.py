from abc import ABC
from posts_app.models import PostModel
from api.classes.type_alias.operations import Operations


class PostOperations(Operations, ABC):

    def __init__(self, request, model_id=None):
        super().__init__(request=request, model_id=model_id, model_class=PostModel)
        self.authenticated_user = self.request_manager.request.user

    # def is_model_from_authenticated_user(self, post_instance=None) -> bool:
    #     return self.request_manager.request.user == post_instance.user if post_instance \
    #         else self.request_manager.request.user == self.model_instance_manager.instance.user
