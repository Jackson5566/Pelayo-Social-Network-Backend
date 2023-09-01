from rest_framework.test import APITestCase
from auth_app.models import User
from rest_framework import status

class Test(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
