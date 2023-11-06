from rest_framework import status
from api.classes.controller_logic_excecutor import ResponseBody
from posts_app.classes.posts_classes.bases.content_operations import ContentListOperations
from posts_app.models import PostModel
from django.shortcuts import get_object_or_404


class AddToContentList(ContentListOperations):

    def __init__(self, request, content_list_id):
        ContentListOperations.__init__(self, request=request, model_id=content_list_id)

    def start_process(self):
        posts_selected_id = self.request_manager.request.data.get('selected_posts')
        posts_unselected_id = self.request_manager.request.data.get('unselected_posts')

        for post_id in posts_selected_id:
            posts_selected = get_object_or_404(PostModel, id=post_id)
            posts_selected.content_list = self.instance_manager.instance
            posts_selected.save()

        for post_id in posts_unselected_id:
            posts_selected = get_object_or_404(PostModel, id=post_id)
            posts_selected.content_list = None
            posts_selected.save()

        self.response = ResponseBody(data={
            'message': "Añadidos"
        }, status=status.HTTP_200_OK)
