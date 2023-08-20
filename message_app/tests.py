from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import MessagesModel
from posts_app.models import PostModel

User = get_user_model()


class GetMessageTest(APITestCase):

    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=user)
        message = MessagesModel(title='Test message', content='Test')
        message.user = user
        message.save()

    def test_create_message_successful(self):
        PostModel.objects.create(title="Titulo", text="Contenido", description="Contenido2")

        data = {'title': 'Titulo', 'content': 'Contenido', 'id': '1'}
        response = self.client.post('/api/message/', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_message_successful(self):
        message_id = MessagesModel.objects.all().first().id
        response = self.client.get(f'/api/message/{message_id}/', format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_message_successful(self):
        message_id = MessagesModel.objects.all().first().id
        response = self.client.put('/api/message/', {'title': 'Titulo', 'content': 'Content', 'id': str(message_id)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
