from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from pc_control.views import RegisterView, FrontendControllerView, ESP32PingView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', obtain_auth_token, name='login'), # DRF Built-in Token generation tool
    path('api/pc-status/', FrontendControllerView.as_view(), name='pc-status'),
    path('api/esp-hardware-check/', ESP32PingView.as_view(), name='esp-check'),
]