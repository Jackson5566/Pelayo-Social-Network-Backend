from posts_app.classes.posts_classes.bases.post_create_update_operations import PostCreateUpdateOperations


class CreatePost(PostCreateUpdateOperations):
    def __init__(self, request):
        super().__init__(request=request)

    def create_or_update_process(self):
        self.create_post()

    def create_post(self):
        self.instance_manager.instance = self.serializer_manager.serializer.create(
            validated_data=self.serializer_manager.serializer.validated_data)

        files_instances = self.create_files()

        self.add_files(files_instances=files_instances)

        self.set_categories()
