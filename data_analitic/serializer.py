# reports/serializers.py

from rest_framework import serializers
from youtube_statement.models import Video

class TopVideoSerializer(serializers.ModelSerializer):
    likeRatio = serializers.SerializerMethodField()
    title = serializers.CharField(source='name')
    thumbnail = serializers.URLField(source='image')
    views = serializers.SerializerMethodField()
    comments = serializers.IntegerField(source='comment_count')
    date = serializers.DateField(source='published_at')

    class Meta:
        model = Video
        fields = ['title', 'thumbnail', 'views', 'comments', 'likeRatio', 'date']

    def get_likeRatio(self, obj):
        if obj.comment_count > 0:
            return round(obj.like_count / obj.comment_count, 2)
        return 0.0

    def get_views(self, obj):
        if obj.view_count >= 1000:
            return f"{round(obj.view_count / 1000)}K"
        return str(obj.view_count)
