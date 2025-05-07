from django.urls import path,include
from rest_framework import routers

from .apis import *

router = routers.DefaultRouter()

router.register('channels',ChannelViewSet)
router.register('channels-select',ChannelSelectViewSet,basename='channels-select')
router.register('videos',VideoViewSet)
router.register('comments',CommentsViewSet)

urlpatterns = [
    path('',include(router.urls)),
]