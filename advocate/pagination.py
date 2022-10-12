from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict, namedtuple



class CustomPageNumberPagination(PageNumberPagination):


    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('total', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('advocates', data)
        ]))