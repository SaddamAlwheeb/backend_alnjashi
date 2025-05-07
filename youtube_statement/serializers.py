from rest_framework import serializers
from .models import Channel, Video, Comment

class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name', 'subtitle', 'description','url', 'image', 
                 'youtube_id', 'subscriber_count', 'view_count', 'video_count','type',
                 'created_at', 'updated_at']


class ChannelSelectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ['id', 'name']

class VideoSerializer(serializers.ModelSerializer):
    channel_name = serializers.CharField(source='channel.name', read_only=True)
    channel_image = serializers.CharField(source='channel.image', read_only=True)
    
    class Meta:
        model = Video
        fields = ['id', 'name', 'image', 'youtube_id', 'description',
                 'view_count', 'like_count', 'comment_count', 'published_at',
                 'channel', 'channel_name','channel_image', 'created_at', 'updated_at']

class CommentSerializer(serializers.ModelSerializer):
    video_title = serializers.CharField(source='video.name', read_only=True)
    channel_name = serializers.CharField(source='video.channel.name', read_only=True)
    channel_image = serializers.CharField(source='video.channel.image', read_only=True)
    category = serializers.IntegerField(source='video.channel.type', read_only=True)
    channel_id = serializers.IntegerField(source='video.channel.id', read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'video', 'video_title', 'channel_name','channel_image','channel_id', 'comment_text','translated_text',
                 'youtube_id', 'user_name', 'user_image', 'like_count',
                 'sentiment', 'sentiment_score','in_bank','category', 'created_at', 'updated_at']