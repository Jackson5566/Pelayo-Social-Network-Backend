from enum import Enum
from rest_framework import status
from api.settings import BASE_DIR
from posts_app.models import FileModel, PostModel
from auth_app.models import User
from rest_framework.test import APITestCase


class PostTestData(Enum):
    TITLE = "Titulo de prueba"
    TEXT = "Texto de prueba"
    DESCRIPTION = "Descripcion de prueba"


def get_post_data() -> dict:
    return {
        'title': PostTestData.TITLE,
        'text': PostTestData.TEXT,
        'description': PostTestData.DESCRIPTION
    }


class PostOperationsTest(APITestCase):

    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=user)

        post = PostModel(**get_post_data())
        post.user = user
        post.save()

        self.post_id = PostModel.objects.all().first().id

    def test_delete_post(self):
        response = self.client.delete(f'/api/posts/{self.post_id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post(self):
        response = self.client.post('/api/posts/', get_post_data())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_post(self):
        response = self.client.get(f'/api/posts/{self.post_id}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post(self):
        data = {'title': 'Nuevo title', 'text': 'Nuevo texto', 'description': 'Nueva descripcion', 'id': self.post_id}
        response = self.client.put(f'/api/posts/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_likes_post(self):
        data = {'like': True, 'likes': 1, 'disslikes': 1, 'id': self.post_id}
        response = self.client.patch(f'/api/posts/{self.post_id}/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_dislikes_post(self):
        data = {'like': False, 'likes': 1, 'disslikes': 1, 'id': self.post_id}
        response = self.client.patch(f'/api/posts/{self.post_id}/', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_file(self):
        nuevo_documento = FileModel()
        file_path = BASE_DIR / 'media/gallery/Michelangelo_-_Creation_of_Adam_cropped.jpg'
        file = open(file_path, 'rb')  # Abre el archivo en modo lectura binaria
        nuevo_documento.files.save('archivo.jpg', file)
        nuevo_documento.save()
        file.close()

        response = self.client.delete(f'/api/posts/delete-file/1/')
        self.assertEqual(response.status_code, 200)
