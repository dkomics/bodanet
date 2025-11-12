from rest_framework import serializers
from .models import Stand

class StandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stand
        fields = ['id', 'name', 'code', 'latitude', 'longitude']
