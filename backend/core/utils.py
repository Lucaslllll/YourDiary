from rest_framework import pagination
from rest_framework.response import Response


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 7
    page_size_query_param = 'page_size'
    max_page_size = 1000