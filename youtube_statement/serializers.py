from rest_framework import serializers
from .models import Channel, Video, Comment

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'subtitle', 'description', 'image', 
                 'youtube_id', 'subscriber_count', 'view_count', 'video_count',
                 'created_at', 'updated_at']


class ChannelSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name']

class VideoSerializer(serializers.ModelSerializer):
    channel_name = serializers.CharField(source='channel.name', read_only=True)
    
    class Meta:
        model = Video
        fields = ['id', 'name', 'image', 'youtube_id', 'description',
                 'view_count', 'like_count', 'comment_count', 'published_at',
                 'channel', 'channel_name', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    video_title = serializers.CharField(source='video.name', read_only=True)
    channel_name = serializers.CharField(source='video.channel.name', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'video', 'video_title', 'channel_name', 'comment_text',
                 'youtube_id', 'author_name', 'author_channel_id', 'like_count',
                 'sentiment', 'sentiment_score', 'created_at', 'updated_at']