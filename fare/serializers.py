from rest_framework import serializers
from .models import FareRule

class FareRuleSerializer(serializers.ModelSerializer):
    origin = serializers.CharField(source='origin.code')
    destination = serializers.CharField(source='destination.code')

    class Meta:
        model = FareRule
        fields = ['origin', 'destination', 'min_fare', 'max_fare', 'recommended_fare', 'updated_at']
