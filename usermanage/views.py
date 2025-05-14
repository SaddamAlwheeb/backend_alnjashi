from django.shortcuts import render
from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import login
from django.contrib.auth.models import User

from .serializers import (
    UserSerializer, UserProfileSerializer, UserRegistrationSerializer,
    LoginSerializer, GitPermissionSerializer
)
from .models import GitPermission, UserProfile

# Registration API
class RegisterAPIView(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login API
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": token.key
        })

# User Profile API
class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        # Return the user's profile
        try:
            return UserProfile.objects.get(user=self.request.user)
        except UserProfile.DoesNotExist:
            # Create profile if it doesn't exist yet
            return UserProfile.objects.create(user=self.request.user)
    
    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

# Git Permissions API
class GitPermissionViewSet(viewsets.ModelViewSet):
    serializer_class = GitPermissionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # For regular users, return only their permissions
        if not self.request.user.is_staff:
            return GitPermission.objects.filter(user=self.request.user)
        # For staff/admin users, return all permissions
        return GitPermission.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    # If user is staff, they can see all permissions
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

# Current User Info API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    data = {
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
    }
    
    # Get user's git permissions
    git_permissions = GitPermission.objects.filter(user=user)
    permissions_data = GitPermissionSerializer(git_permissions, many=True).data
    
    data['git_permissions'] = permissions_data
    
    return Response(data)
