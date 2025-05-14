from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views as token_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include('youtube_statement.urls')),
    path("api/", include('data_analitic.urls')),
    path("api/auth/", include('usermanage.urls')),
    path("api/token/", token_views.obtain_auth_token, name='api-token'),
]
