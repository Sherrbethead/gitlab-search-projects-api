import requests
from django.db import models


class SearchData(models.Model):
    """Searching information database table."""
    search_query = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.search_query

    @classmethod
    def parse_data(cls, search_query):
        """
        Parse JSON gitlab data by entered query
        and put it to created model instances.
        """
        raw_data = requests.get(
            f'https://gitlab.com/api/v4/projects/?search={search_query}'
        ).json()
        if not raw_data:
            raise(ValueError('There are no projects for this search query'))

        # Create query set for entered query
        search_data = cls.objects.create(search_query=search_query)
        # Create and relate query set for each found gitlab project
        for project in raw_data:
            GitlabData.objects.create(
                project_id=project['id'],
                name=project['name'],
                description=project['description'],
                last_activity_at=project['last_activity_at'],
                search_data=search_data
            )
        return search_data


class GitlabData(models.Model):
    """Gitlab projects database table."""
    project_id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    last_activity_at = models.DateTimeField()
    search_data = models.ForeignKey(SearchData, on_delete=models.CASCADE,
                                    related_name='gitlab_data')

    def __str__(self):
        return f'"{self.name}" project with ID {self.project_id}'
