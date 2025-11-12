from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def ping(request):
    return Response({"message": "bodanet alive"})


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Stand
from .serializers import StandSerializer

@api_view(['GET'])
def list_stands(request):
    stands = Stand.objects.all().order_by('name')
    serializer = StandSerializer(stands, many=True)
    return Response(serializer.data)
