from api.base_test import *


class ComplaintTest(Test):
    def setUp(self):
        super().setUp()

    def test_complaint_same_user(self):
        user_id = User.objects.all().first().id
        data = {'id': user_id}
        response = self.client.post(f'/api/denunciate/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_complaint_user(self):
        user = User.objects.create_user(username="preuba", password="prueba", email="prueba@gmail.com")
        data = {'id': user.id}
        response = self.client.post(f'/api/denunciate/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_complaint_complained_user(self):
        user = User.objects.create_user(username="preuba2", password="prueba2", email="prueba2@gmail.com")
        user.denunciations.add(self.user)
        data = {'id': user.id}
        response = self.client.post(f'/api/denunciate/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
