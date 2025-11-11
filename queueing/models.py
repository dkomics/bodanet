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
