from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, filters
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings
from .models import Comment, Video
from .serializers import *
import os

# Get API key from environment variables
API_KEY = os.getenv('YOUTUBE_API_KEY', settings.YOUTUBE_API_KEY)

from rest_framework import viewsets
from .models import *
from .serializers import *
from utlis.utils import get_youtube_comments
from .filters import ChannelFilter , CommentFilter ,VideoFilter

class ChannelViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ChannelFilter
    filterset_fields = ['name', 'subscriber_count']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'subscriber_count', 'created_at']

class ChannelSelectViewSet(viewsets.ModelViewSet):
    queryset = Channel.objects.all()
    serializer_class = ChannelSelectSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = VideoFilter
    filterset_fields = ['channel', 'name', 'view_count']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'view_count', 'published_at']

    def create(self, request, *args, **kwargs):
        # أولاً: احفظ الفيديو الجديد
        
        response = super().create(request, *args, **kwargs)
        video_id = response.data.get('youtube_id')
        
        try:
            video = Video.objects.get(youtube_id=video_id)
            items = get_youtube_comments(video_id)

            if items:
                comments_to_create = []
                for item in items:
                    comment = item['snippet']['topLevelComment']['snippet']
                    comments_to_create.append(Comment(
                        video=video,
                        youtube_id=item['id'],
                        comment_text=comment['textDisplay'],
                        user_name=comment['authorDisplayName'],
                        author_channel_id=comment.get('authorChannelId', {}).get('value'),
                        like_count=comment.get('likeCount', 0)
                    ))
                Comment.objects.bulk_create(comments_to_create, ignore_conflicts=True)
        except Exception as e:
            print(f"تعذر جلب التعليقات: {e}")

        return response

class CommentsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = CommentFilter
    filterset_fields = ['video', 'sentiment', 'user_name']
    search_fields = ['comment_text', 'user_name']
    ordering_fields = ['created_at', 'like_count', 'sentiment_score']
