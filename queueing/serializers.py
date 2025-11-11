from rest_framework import serializers
from .models import StandSession

class StandSessionSerializer(serializers.ModelSerializer):
    rider_username = serializers.CharField(source='rider.username')
    stand_code = serializers.CharField(source='stand.code')

    class Meta:
        model = StandSession
        fields = ['id', 'rider_username', 'stand_code', 'joined_at', 'active']
