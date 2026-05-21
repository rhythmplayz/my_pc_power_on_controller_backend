from django.db import models
from django.utils import timezone
from datetime import timedelta

class PCController(models.Model):
    name = models.CharField(max_length=100, default="My PC")
    is_permitted = models.BooleanField(default=False)
    
    # 1. Change auto_now=True to null=True, blank=True
    last_seen_by_esp = models.DateTimeField(null=True, blank=True)

    @property
    def is_esp_online(self):
        # 2. If it has never pinged, it is explicitly Offline
        if not self.last_seen_by_esp:
            return False
        return timezone.now() - self.last_seen_by_esp < timedelta(minutes=5)

    def __str__(self):
        return f"{self.name} - Permitted: {self.is_permitted} - Online: {self.is_esp_online}"