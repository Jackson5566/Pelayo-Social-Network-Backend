from api.base_test import *


class PostsGetTest(Test):
    def setUp(self):
        super().setUp()

    def test_get_posts_successful(self):
        response = self.client.get('/api/posts/allposts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_searched_posts_successful(self):
        response = self.client.get('/api/posts/search/?search=hola')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pre_search_successful(self):
        response = self.client.get('/api/posts/pre-search')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_categories_successful(self):
        response = self.client.get('/api/posts/get-categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
