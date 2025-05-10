from django.urls import path

from data_analitic.reports import *


urlpatterns = [
    path('summary-stats', summary_stats, name='summary_stats'),
    path('comments-over-time', comments_over_time, name='comments_over_time'),
    path('top-content/', TopContentAPIView.as_view(), name='top-content'),
]