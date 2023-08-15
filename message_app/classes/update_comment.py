from api.decorators.validate_serializer import validate_serializer
from .create_update_comment_operations import CreateUpdateCommentOperations


class UpdateCommentOperation(CreateUpdateCommentOperations):
    def __init__(self, request):
        comment_id = request.data.get('id')
        super().__init__(request=request, model_id=comment_id)

    @validate_serializer('comment_serializer_manager')
    def create_or_update_process(self):
        self.model_instance_manager.instance = self.comment_serializer_manager.serializer.update(
            instance=self.model_instance_manager.instance,
            validated_data=self.comment_serializer_manager.serializer.validated_data)
