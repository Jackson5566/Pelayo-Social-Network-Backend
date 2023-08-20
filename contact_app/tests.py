from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class SendMailOperationTest(APITestCase):

    def test_send_mail_successful(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=user)

        data = {'subject': 'Test Subject', 'content': 'Test Content'}
        response = self.client.post('/api/enviar-mail', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
