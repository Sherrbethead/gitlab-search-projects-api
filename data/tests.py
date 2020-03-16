import requests
from django.test import TestCase
from data import models


class ModelTest(TestCase):

    def test_search_data_str(self):
        """Test search data string representation"""
        search_data = models.SearchData.objects.create(
            search_query='kremlin'
        )

        self.assertEqual(str(search_data), f'{search_data.search_query}')

    def test_gitlab_data_str(self):
        """Test gitlab data string representation"""
        search_data = models.SearchData.objects.create(
            search_query='kremlin'
        )
        gitlab_data = models.GitlabData.objects.create(
            project_id=1,
            name='Kremlin',
            description='Sample',
            last_activity_at='2019-12-12T22:30:52.878000+03:00',
            search_data=search_data
        )

        self.assertEqual(
            str(gitlab_data),
            f'"{gitlab_data.name}" project with ID {gitlab_data.project_id}'
        )

    def test_parse_data_success(self):
        """Requested projects are found."""

        search_query = 'kremlin'
        raw_data = requests.get(
            f'https://gitlab.com/api/v4/projects/?search={search_query}'
        ).json()

        search_data = models.SearchData.parse_data(search_query)
        gitlab_data = models.GitlabData.objects.all()

        self.assertEqual(search_query, search_data.search_query)
        self.assertEqual(len(raw_data), len(gitlab_data))

    def test_parse_data_failed(self):
        """Requested projects are not found."""

        try:
            models.SearchData.parse_data('33trgdbgbnm')
        except ValueError:
            pass
        else:
            raise AssertionError("ValueError was not raised")
