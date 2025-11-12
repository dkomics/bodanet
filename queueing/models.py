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
    """
    A record of a rider being assigned from a stand.
    """
    rider = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stand = models.ForeignKey('core.Stand', on_delete=models.SET_NULL, null=True, blank=True)
    requested_at = models.DateTimeField(default=timezone.now)
    trusted_only = models.BooleanField(default=False)
    # you can add destination later if you start collecting it
    # destination = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return f"Trip: {self.rider} from {self.stand} at {self.requested_at}"
