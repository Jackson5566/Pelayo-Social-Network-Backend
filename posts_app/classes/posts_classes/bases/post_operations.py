from api.classes.view_logic_executor import ControllerLogicExecutor


class PostOperations(ControllerLogicExecutor):

    def __init__(self, post_instance, request):
        super().__init__(request=request)
        self.post_instance = post_instance

    def start_process(self) -> None:
        pass

    def is_post_from_authenticated_user(self, post_instance=None) -> bool:
        return self.request_manager.request.user == post_instance.user if post_instance \
            else self.request_manager.request.user == self.post_instance.user
