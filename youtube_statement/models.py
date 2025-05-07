from django.db import models
from .choice import *

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Channel(BaseModel):
    name = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    url = models.URLField(max_length=500)
    image = models.URLField(max_length=500)
    youtube_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    subscriber_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    video_count = models.IntegerField(default=0)
    type = models.IntegerField(choices=ChannelTypeStat.choices , default= ChannelTypeStat.youtub)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-subscriber_count']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['youtube_id']),
        ]
    
class Video(BaseModel):
    channel = models.ForeignKey(Channel, related_name="videos", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.URLField(max_length=500)
    youtube_id = models.CharField(max_length=100)
    duration = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    view_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-published_at']
        indexes = [
            models.Index(fields=['youtube_id']),
            models.Index(fields=['name']),
        ]

class Comment(BaseModel):
    video = models.ForeignKey(Video, related_name="comments", on_delete=models.CASCADE)
    comment_text = models.TextField()
    translated_text = models.TextField(null=True ,blank=True)
    youtube_id = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100,null =True, blank=True)
    author_channel_id  = models.CharField(max_length=100,null =True, blank=True)
    user_image = models.CharField(max_length=2500, blank=True, null=True)
    like_count = models.IntegerField(default=0)
    sentiment = models.IntegerField(choices=CommentState.choices, default=CommentState.neutral)
    sentiment_score = models.FloatField(default=0.0)
    in_bank = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user_name}: {self.comment_text[:50]}..."

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['youtube_id']),
            models.Index(fields=['sentiment']),
            models.Index(fields=['created_at']),
        ]