from django.db import models
from django.utils import timezone
from datetime import timedelta

class PCController(models.Model):
    name = models.CharField(max_length=100, default="My PC")
    is_permitted = models.BooleanField(default=False)  # 0 or 1
    last_seen_by_esp = models.DateTimeField(auto_now=True)

    @property
    def is_esp_online(self):
        # Calculates if the ESP32 checked in during the last 5 minutes
        if not self.last_seen_by_esp:
            return False
        return timezone.now() - self.last_seen_by_esp < timedelta(minutes=5)

    def __str__(self):
        return f"{self.name} - Permitted: {self.is_permitted} - Online: {self.is_esp_online}"