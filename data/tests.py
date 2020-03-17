import json
from urllib.request import urlopen
from django.test import TestCase
from data.models import SearchData, GitlabData


def get_gitlab_data(search_query):
    """Use function with native Python parser library."""
    parse_url = f'https://gitlab.com/api/v4/projects/?search={search_query}'

    with urlopen(parse_url) as raw:
        return json.loads(raw.read())


class ModelTest(TestCase):

    def setUp(self):
        SearchData.objects.create(search_query='kremlin')
        SearchData.objects.create(search_query='whitehouse')

    def test_search_data_str(self):
        """Test search data string representation."""
        kremlin = SearchData.objects.get(search_query='kremlin')
        whitehouse = SearchData.objects.get(search_query='whitehouse')

        self.assertEqual(str(kremlin), f'{kremlin.search_query}')
        self.assertEqual(str(whitehouse), f'{whitehouse.search_query}')

    def test_gitlab_data_str(self):
        """Test gitlab data string representation."""
        kremlin = SearchData.objects.get(search_query='kremlin')
        whitehouse = SearchData.objects.get(search_query='whitehouse')

        kremlin_data = GitlabData.objects.create(
            project_id=1,
            name='Kremlin',
            description='Sample1',
            last_activity_at='2019-12-12T22:30:52.878000+03:00',
            search_data=kremlin
        )
        whitehouse_data = GitlabData.objects.create(
            project_id=2,
            name='Whitehouse',
            description='Sample2',
            last_activity_at='2019-12-13T21:16:15.844000+03:00',
            search_data=whitehouse
        )

        self.assertEqual(
            str(kremlin_data),
            f'"{kremlin_data.name}" project with ID {kremlin_data.project_id}'
        )
        self.assertEqual(
            str(whitehouse_data),
            f'"{whitehouse_data.name}" '
            f'project with ID {whitehouse_data.project_id}'
        )

    def test_parse_data_success(self):
        """Requested projects are found."""
        kremlin = SearchData.objects.get(search_query='kremlin')
        whitehouse = SearchData.objects.get(search_query='whitehouse')

        search_queries = [kremlin.search_query, whitehouse.search_query]
        for search_query in search_queries:
            raw_data = get_gitlab_data(search_query)
            search_data_one = SearchData.parse_data(search_query)
            gitlab_data = GitlabData.objects.filter(
                search_data=search_data_one
            )

            self.assertEqual(search_query, search_data_one.search_query)
            self.assertEqual(len(raw_data), len(gitlab_data))

            # Retry same query
            search_data_two = SearchData.parse_data(search_query)
            gitlab_data = GitlabData.objects.filter(
                search_data=search_data_two
            )

            self.assertEqual(search_query, search_data_two.search_query)
            self.assertEqual(len(raw_data), len(gitlab_data))
            self.assertEqual(search_data_one.id, search_data_two.id)
            self.assertNotEqual(
                search_data_one.created_at, search_data_two.created_at
            )

    def test_parse_data_failed(self):
        """Requested projects are not found."""
        test_cases = ['33trgdbgbnm', 'efggrhhj///', 'WDWFWEG']

        try:
            for query in test_cases:
                SearchData.parse_data(query)
        except ValueError:
            pass
        else:
            raise AssertionError("ValueError was not raised")
