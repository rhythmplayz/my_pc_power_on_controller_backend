from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class ControlUser(AbstractUser):
    """
    Custom user model for the PC Control system.
    Inherits standard authentication fields (username, password, email).
    """
    
    is_verified = models.BooleanField(
        default=False, 
        help_text="Designates whether this user has been verified by an admin."
    )
    
    class Meta:
        verbose_name = "Control User"
        verbose_name_plural = "Control Users"

    def __str__(self):
        return self.username

class DeviceControlState(models.Model):
    """
    Single state tracker for the PC power intention and ESP32 heartbeat connectivity.
    """
    # Tracks who owns or last altered this machine control configuration
    user = models.ForeignKey(
        ControlUser, 
        on_delete=models.CASCADE, 
        related_name="device_states"
    )
    
    # PC Tracking: Do I want to turn on my PC or not?
    should_power_on = models.BooleanField(
        default=False,
        help_text="True if the user intends to boot the PC, False otherwise."
    )
    
    # ESP32 Tracking: Automatically calculated via heartbeats sent every 5 minutes
    last_heartbeat = models.DateTimeField(
        default=timezone.now,
        help_text="The exact time the ESP32 last pinged the REST API."
    )

    class Meta:
        verbose_name = "Device Control State"
        verbose_name_plural = "Device Control States"

    @property
    def is_esp32_online(self):
        """
        Dynamically calculates if the ESP32 is online.
        Returns True if a heartbeat was received within the last 5 minutes (plus a 10s buffer).
        """
        now = timezone.now()
        time_difference = now - self.last_heartbeat
        return time_difference.total_seconds() <= (5 * 60 + 10)

    def __str__(self):
        status = "ONLINE" if self.is_esp32_online else "OFFLINE"
        return f"{self.user.username}'s Rig Control (ESP32: {status} | PC Power Target: {self.should_power_on})"