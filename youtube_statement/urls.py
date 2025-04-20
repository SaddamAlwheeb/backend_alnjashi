from django.urls import path,include
from rest_framework import routers

from .apis import fetch_comments
from .apis import *

router = routers.DefaultRouter()

router.register('channels',ChannelViewSet)
router.register('channels-select',ChannelSelectViewSet,basename='channels-select')
router.register('videos',VideoViewSet)
router.register('comments',CommentsViewSet)

urlpatterns = [
    path('fetch_comments/<str:video_id>/', fetch_comments, name='fetch_comments'),
    path('',include(router.urls)),
]