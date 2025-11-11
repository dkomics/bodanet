from django.db import models
from core.models import User, Stand

class RiderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='riderprofile')
    stand = models.ForeignKey(Stand, on_delete=models.SET_NULL, null=True, blank=True)
    is_trusted = models.BooleanField(default=False)
    plate_number = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} ({'trusted' if self.is_trusted else 'untrusted'})"
