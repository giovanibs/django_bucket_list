from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bucketapp.urls')),
    path('', include('userapp.urls')),
]
