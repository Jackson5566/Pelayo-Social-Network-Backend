from api.base_test import *


class GetUserInfoTest(Test):
    def setUp(self):
        super().setUp()

    def test_get_selected_user_info(self):
        user = User.objects.create_user(username='testuser2', password='testpass2', email="flowme@gmail.com")
        user_id = user.id
        response = self.client.get(f'/api/user/{user_id}/?only=posts')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_current_user_info(self):
        response = self.client.get(f'/api/current-user-information/?only=posts')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_current_user_info(self):
        response = self.client.get(f'/api/current-user-information/?only=info')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
