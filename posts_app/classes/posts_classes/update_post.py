from posts_app.classes.posts_classes.bases.post_create_update_operations import PostCreateUpdateOperations


class UpdatePost(PostCreateUpdateOperations):

    def __init__(self, request, post_id: int):
        super().__init__(request=request, model_id=post_id)

    def create_or_update_process(self):
        if self.is_model_instance_from_user(user=self.authenticated_user):
            self.update_post()

        else:
            raise Exception("Prohibido hacer la operación")

    def update_post(self):
        files_instances = self.create_files()

        self.instance_manager.instance = self.serializer_manager.serializer.update(
            validated_data=self.serializer_manager.serializer.validated_data,
            instance=self.instance_manager.instance)

        self.add_files(files_instances=files_instances)

        self.instance_manager.instance.categories.clear()
        self.set_categories()
