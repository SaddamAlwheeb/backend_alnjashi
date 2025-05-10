from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from youtube_statement.models import *
from .serializer import TopVideoSerializer

@api_view(['GET'])
def summary_stats(request):
    return Response({
        "channels_count": Channel.objects.count(),
        "videos_count": Video.objects.count(),
        "comments_count": Comment.objects.count(),
        "positive_comments": Comment.objects.filter(sentiment=1).count(),
        "neutral_comments": Comment.objects.filter(sentiment=3).count(),
        "negative_comments": Comment.objects.filter(sentiment=2).count(),
    })


@api_view(['GET'])
def comments_over_time(request):
    data = (Comment.objects
        .annotate(date=models.functions.TruncMonth('created_at'))
        .values('date')
        .annotate(count=models.Count('id'))
        .order_by('date'),)
    return Response(data)


class TopContentAPIView(APIView):
    def get(self, request):
        top_videos = Video.objects.all().order_by('-view_count')[:5]
        serializer = TopVideoSerializer(top_videos, many=True)
        return Response(serializer.data)