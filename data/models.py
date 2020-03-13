from django.db import models


class GitlabData(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    last_activity_at = models.DateTimeField()


class SearchData(models.Model):
    search_query = models.CharField(max_length=255)
    gitlab_data = models.ForeignKey(GitlabData, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.search_query
