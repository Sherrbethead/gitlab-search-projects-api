from rest_framework import serializers
from .models import SearchData, GitlabData


class GitlabDataSerializer(serializers.ModelSerializer):
    """Render JSON/Python data of gitlab projects fields."""
    # Convert representation name
    id = serializers.IntegerField(source='project_id')

    class Meta:
        model = GitlabData
        fields = ('id', 'name', 'description', 'last_activity_at')
        read_only_fields = ('id', 'name', 'description', 'last_activity_at')


class SearchDataSerializer(serializers.ModelSerializer):
    """Render JSON/Python data of searching data fields."""
    # Nest gitlab projects into searching data field
    gitlab_data = GitlabDataSerializer(many=True, read_only=True)

    class Meta:
        model = SearchData
        fields = ('id', 'search_query', 'gitlab_data', 'created_at')
        read_only_fields = ('id', 'gitlab_data', 'created_at')
