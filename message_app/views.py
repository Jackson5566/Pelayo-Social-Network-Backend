from rest_framework.views import APIView
from message_app.classes.create_comment import CreateCommentOperation
from message_app.classes.update_comment import UpdateCommentOperation
from message_app.classes.get_comment import GetCommentOperation
from api.shortcuts.data_get import process_and_get_response
from api.decorators.add_security import access_protected
from message_app.classes.delete_comment_operation import DeleteCommentOperation

from api.serializers import CommentBaseSerializer
from rest_framework import generics
from .paginations import MessagesPagination
from posts_app.models import PostModel


@access_protected
class MessageView(APIView):
    def post(self, request):
        create_comment_instance = CreateCommentOperation(request=request)
        return process_and_get_response(create_comment_instance)

    def put(self, request):
        update_comment_instance = UpdateCommentOperation(request=request)
        return process_and_get_response(update_comment_instance)

    def get(self, request, id):
        get_comment_instance = GetCommentOperation(request=request, post_id=id)
        return process_and_get_response(get_comment_instance)

    def delete(self, request, id):
        delete_comment_instance = DeleteCommentOperation(request=request, model_id=id)
        return process_and_get_response(delete_comment_instance)


@access_protected
class CommentsView(generics.ListAPIView):
    serializer_class = CommentBaseSerializer
    pagination_class = MessagesPagination

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        post_messages = PostModel.objects.get(id=post_id).messages.all()
        return post_messages
