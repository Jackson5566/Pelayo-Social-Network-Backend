from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MyPagination(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'

    def get_paginated_response(self, data):
        response = {
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        }
        if self.request.query_params.get('only') == 'posts':
            response = response.get('results', '')

        return Response(response)
