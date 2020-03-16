from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin
)
from rest_framework.response import Response
from rest_framework import status
from .models import SearchData
from .serializers import SearchDataSerializer


class SearchDataView(ListModelMixin,
                     CreateModelMixin,
                     RetrieveModelMixin,
                     DestroyModelMixin,
                     GenericViewSet):
    """
    API endpoint that allows to search Gitlab projects by entered query.
    """
    queryset = SearchData.objects.all()
    serializer_class = SearchDataSerializer

    def create(self, request, *args, **kwargs):
        """Override POST request with the aim of gitlab data handling."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            parsed_data = SearchData.parse_data(**serializer.validated_data)
        except ValueError as exp:
            content = {'error': f'{exp}'}  # no gitlab projects
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(parsed_data)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)
