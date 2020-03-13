import requests
from rest_framework import serializers
from .models import SearchData, GitlabData


# class GitlabData(object):
#     def __init__(self, id, name, description, last_activity_at):
#         self.id = id
#         self.name = name
#         self.description = description
#         self.last_activity_at = last_activity_at


class GitlabDataSerializer(serializers.PrimaryKeyRelatedField, serializers.ModelSerializer):

    class Meta:
        model = GitlabData
        fields = ('id', 'name', 'description', 'last_activity_at')


class SearchDataSerializer(serializers.ModelSerializer):
    gitlab_data = GitlabDataSerializer(read_only=True)

    class Meta:
        model = SearchData
        fields = ('search_query', 'gitlab_data', 'created_at')
