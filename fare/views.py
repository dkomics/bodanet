from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from core.models import Stand
from .models import FareRule
from .serializers import FareRuleSerializer

@api_view(['GET'])
def get_fare(request):
    origin_code = request.query_params.get('origin')
    destination_code = request.query_params.get('destination')

    if not origin_code or not destination_code:
        return Response(
            {"detail": "origin and destination query params are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        origin = Stand.objects.get(code=origin_code)
    except Stand.DoesNotExist:
        return Response({"detail": f"origin stand '{origin_code}' not found"}, status=404)

    try:
        destination = Stand.objects.get(code=destination_code)
    except Stand.DoesNotExist:
        return Response({"detail": f"destination stand '{destination_code}' not found"}, status=404)

    try:
        rule = FareRule.objects.get(origin=origin, destination=destination)
    except FareRule.DoesNotExist:
        return Response(
            {"detail": "no fare rule for this route"},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = FareRuleSerializer(rule)
    return Response(serializer.data)
