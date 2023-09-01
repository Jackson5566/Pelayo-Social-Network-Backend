from api.base_test import *


class SendMailOperationTest(Test):
    def setUp(self):
        super().setUp()

    def test_send_mail_successful(self):
        data = {'subject': 'Test Subject', 'content': 'Test Content'}
        response = self.client.post('/api/enviar-mail', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
