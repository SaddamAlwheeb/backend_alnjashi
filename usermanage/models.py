from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class GitPermission(models.Model):
    PERMISSION_CHOICES = (
        ('read', 'Read'),
        ('write', 'Write'),
        ('admin', 'Admin'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='git_permissions')
    repository_name = models.CharField(max_length=255)
    repository_url = models.URLField()
    permission_type = models.CharField(max_length=10, choices=PERMISSION_CHOICES, default='read')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'repository_name')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.repository_name} - {self.permission_type}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    avatar = models.URLField(blank=True, null=True)
    github_username = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username
