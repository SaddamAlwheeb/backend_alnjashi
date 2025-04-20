import django_filters
from .models import Channel, Video, Comment

class ChannelFilter(django_filters.FilterSet):
    class Meta:
        model = Channel
        fields = '__all__'  # ← جميع الحقول قابلة للفلترة بشكل تلقائي

class VideoFilter(django_filters.FilterSet):
    class Meta:
        model = Video
        fields = '__all__'

class CommentFilter(django_filters.FilterSet):
    class Meta:
        model = Comment
        fields = '__all__'
