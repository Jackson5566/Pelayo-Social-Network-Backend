from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from message_app.classes.create_comment import CreateCommentOperation
from message_app.classes.update_comment import UpdateCommentOperation
from message_app.classes.get_comment import GetCommentOperation


class MessageView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        create_comment_instance = CreateCommentOperation(request=request)
        create_comment_instance.start_process()
        return create_comment_instance.response

    def put(self, request):
        update_comment_instance = UpdateCommentOperation(request=request)
        update_comment_instance.start_process()
        return update_comment_instance.response

    def get(self, request, id):
        get_comment_instance = GetCommentOperation(request=request, post_id=id)
        get_comment_instance.start_process()
        return get_comment_instance.response
