from django.db import models
from core.models import Stand

class FareRule(models.Model):
    origin = models.ForeignKey(
        Stand,
        on_delete=models.CASCADE,
        related_name='fare_origins'
    )
    destination = models.ForeignKey(
        Stand,
        on_delete=models.CASCADE,
        related_name='fare_destinations'
    )
    min_fare = models.PositiveIntegerField()
    max_fare = models.PositiveIntegerField()
    recommended_fare = models.PositiveIntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('origin', 'destination')

    def __str__(self):
        return f"{self.origin.code} -> {self.destination.code} ({self.recommended_fare})"
