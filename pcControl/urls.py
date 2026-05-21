# pcControl/urls.py
from django.urls import path
from .views import ESP32HeartbeatAPIView, LoginAPIView, RegisterAPIView, UIControlAPIView

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='api_login'),
    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('control/', UIControlAPIView.as_view(), name='ui_control'),
    path('esp32/heartbeat/', ESP32HeartbeatAPIView.as_view(), name='esp32_heartbeat'),
]