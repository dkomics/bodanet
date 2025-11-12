from django.db import models
from django.utils import timezone
from core.models import Stand, User

class StandSession(models.Model):
    """
    A rider 'checks in' to a stand and is considered available for jobs.
    """
    rider = models.ForeignKey(User, on_delete=models.CASCADE)
    stand = models.ForeignKey(Stand, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['joined_at']

    def __str__(self):
        return f"{self.rider} @ {self.stand} ({'active' if self.active else 'inactive'})"

from django.conf import settings

class Trip(models.Model):
    rider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stand = models.ForeignKey(Stand, on_delete=models.SET_NULL, null=True, blank=True)
   
    destination_stand = models.ForeignKey(
        Stand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='destination_trips'
    )
    destination_text = models.CharField(max_length=200, blank=True, null=True)

    requested_at = models.DateTimeField(default=timezone.now)
    trusted_only = models.BooleanField(default=False)

    def __str__(self):
        dest = self.destination_stand.code if self.destination_stand else (self.destination_text or "unknown")
        return f"Trip: {self.rider} from {self.stand} to {dest} at {self.requested_at}"