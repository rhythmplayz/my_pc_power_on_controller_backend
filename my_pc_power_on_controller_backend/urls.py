# your_project_folder/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('pcControl.urls')), # Routes login to: /api/login/
]