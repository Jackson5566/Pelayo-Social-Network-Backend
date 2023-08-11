from api.classes.view_logic_executor import ViewLogicExecutor


class PostOperations(ViewLogicExecutor):

    def __init__(self, post_instance, request):
        super().__init__(request=request)
        self.post_instance = post_instance

    def start_process(self) -> None:
        pass

    def is_post_from_authenticated_user(self, post_instance=None) -> bool:
        return self.request.user == post_instance.user or self.post_instance.user
