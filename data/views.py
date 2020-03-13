import requests
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from .models import SearchData, GitlabData
from .serializers import GitlabDataSerializer, SearchDataSerializer


class SearchDataView(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = SearchData.objects.all()
    serializer_class = SearchDataSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    # def get_queryset(self):
    #     gitlab_data = GitlabData.objects.all()
    #     queryset = None
    #     for data in gitlab_data:
    #         queryset = GitlabData.objects.filter(
    #             queue=data
    #         )
    #
    #     return queryset

    def post(self, request, *args, **kwargs):
        search_query = request.data.get('search_query')
        raw_data = requests.get(
                    f'https://gitlab.com/api/v4/projects/?search={search_query}'
                ).json()
        for project in raw_data:
            data = {
                'id': project['id'],
                'name': project['name'],
                'description': project['description'],
                'last_activity_at': project['last_activity_at']
            }
            serializer = GitlabDataSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

        return self.create(request, *args, **kwargs)
