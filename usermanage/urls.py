from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterAPIView, LoginAPIView, UserProfileAPIView, 
    GitPermissionViewSet, get_current_user
)

router = DefaultRouter()
router.register(r'git-permissions', GitPermissionViewSet, basename='git-permissions')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('profile/', UserProfileAPIView.as_view(), name='profile'),
    path('me/', get_current_user, name='current-user'),
]
