from .create_update_comment_operations import CreateUpdateCommentOperations


class UpdateCommentOperation(CreateUpdateCommentOperations):
    def __init__(self, request):
        comment_id = request.data.get('id')
        super().__init__(request=request, model_id=comment_id)

    def create_or_update_process(self):
        self.instance_manager.instance = self.serializer_manager.serializer.update(
            instance=self.instance_manager.instance,
            validated_data=self.serializer_manager.serializer.validated_data)
