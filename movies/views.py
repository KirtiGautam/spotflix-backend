from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from movies import api_helper


class Trending(viewsets.ViewSet):
    permission_classes = [AllowAny]

    def top(self, request):

        data = api_helper.trending_media(self.request.query_params.get('page') or 1)

        return Response(data)