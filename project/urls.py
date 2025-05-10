from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/",include('youtube_statement.urls')),
    path("api/",include('data_analitic.urls'))
]
