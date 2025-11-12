from rest_framework import serializers
from .models import StandSession, Trip

class TripSerializer(serializers.ModelSerializer):
    rider_username = serializers.CharField(source='rider.username', read_only=True)
    stand_code = serializers.CharField(source='stand.code', read_only=True)
    destination_stand_code = serializers.CharField(source='destination_stand.code', read_only=True)

    class Meta:
        model = Trip
        fields = [
            'id',
            'rider_username',
            'stand_code',
            'destination_stand_code',
            'destination_text',
            'trusted_only',
            'requested_at',
        ]