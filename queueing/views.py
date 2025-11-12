from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.utils import timezone

from core.models import Stand, User
from trusted.models import RiderProfile   # we'll make sure this exists
from .models import StandSession, Trip
from .serializers import TripSerializer

@api_view(['POST'])
def join_queue(request):
    user = request.user
    if not user.is_authenticated:
        return Response({"detail": "authentication required"}, status=status.HTTP_401_UNAUTHORIZED)

    if not getattr(user, 'is_rider', False):
        return Response({"detail": "only riders can join the queue"}, status=status.HTTP_403_FORBIDDEN)

    stand_code = request.data.get('stand_code')
    if not stand_code:
        return Response({"detail": "stand_code is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        stand = Stand.objects.get(code=stand_code)
    except Stand.DoesNotExist:
        return Response({"detail": "stand not found"}, status=status.HTTP_404_NOT_FOUND)

    # 1) check if rider already has an active session (any stand, or you can filter by this stand)
    existing = StandSession.objects.filter(rider=user, active=True).first()
    if existing:
        # optionally update stand if rider moved stands
        if existing.stand != stand:
            existing.stand = stand
            existing.joined_at = timezone.now()
            existing.save()
        # return existing session
        return Response({
            "id": existing.id,
            "rider_username": user.username,
            "stand_code": existing.stand.code,
            "joined_at": existing.joined_at,
            "active": existing.active
        }, status=status.HTTP_200_OK)

    # 2) otherwise create a new session
    session = StandSession.objects.create(
        rider=user,
        stand=stand,
        joined_at=timezone.now(),
        active=True
    )

    return Response({
        "id": session.id,
        "rider_username": user.username,
        "stand_code": stand.code,
        "joined_at": session.joined_at,
        "active": session.active
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def next_rider(request):
    stand_code = request.data.get('stand_code')
    trusted_only = request.data.get('trusted_only', False)
    destination_code = request.data.get('destination_code')
    destination_text = request.data.get('destination_text')

    if not stand_code:
        return Response({"detail": "stand_code is required"}, status=400)

    try:
        stand = Stand.objects.get(code=stand_code)
    except Stand.DoesNotExist:
        return Response({"detail": "stand not found"}, status=404)

    qs = StandSession.objects.filter(stand=stand, active=True).order_by('joined_at')

    if trusted_only:
        qs = qs.filter(rider__riderprofile__is_trusted=True)

    session = qs.first()
    if not session:
        return Response({"detail": "no available rider"}, status=404)

    # deactivate session
    session.active = False
    session.save()

    # try to resolve destination stand (optional)
    destination_stand = None
    if destination_code:
        try:
            destination_stand = Stand.objects.get(code=destination_code)
        except Stand.DoesNotExist:
            destination_stand = None  # we'll just use text if provided

    # create trip record
    Trip.objects.create(
        rider=session.rider,
        stand=stand,
        destination_stand=destination_stand,
        destination_text=destination_text,
        trusted_only=bool(trusted_only),
    )

    data = {
        "rider_id": session.rider.id,
        "rider_username": session.rider.username,
        "rider_phone": session.rider.phone,
        "stand": stand.code,
        "trusted": getattr(getattr(session.rider, 'riderprofile', None), 'is_trusted', False),
        # echo back destination so client knows what got recorded
        "destination_stand": destination_stand.code if destination_stand else None,
        "destination_text": destination_text,
    }
    return Response(data, status=200)



@api_view(['POST'])
def complete_trip(request):
    """
    v1 placeholder: rider can rejoin after trip.
    For now we just accept a session_id and mark inactive.
    """
    session_id = request.data.get('session_id')
    if not session_id:
        return Response({"detail": "session_id is required"}, status=400)

    try:
        session = StandSession.objects.get(id=session_id)
    except StandSession.DoesNotExist:
        return Response({"detail": "session not found"}, status=404)

    session.active = False
    session.save()
    return Response({"detail": "session closed"}, status=200)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_trips(request):
    qs = Trip.objects.all().order_by('-requested_at')

    stand_code = request.query_params.get('stand')
    if stand_code:
        qs = qs.filter(stand__code=stand_code)

    rider_username = request.query_params.get('rider')
    if rider_username:
        qs = qs.filter(rider__username=rider_username)

    trusted_only = request.query_params.get('trusted_only')
    if trusted_only is not None:
        qs = qs.filter(trusted_only=trusted_only.lower() == 'true')

    page_size = int(request.query_params.get('page_size', 50))
    page = int(request.query_params.get('page', 1))
    start = (page - 1) * page_size
    end = start + page_size

    serializer = TripSerializer(qs[start:end], many=True)
    return Response(serializer.data, status=200)
