from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from core.models import Stand, User
from trusted.models import RiderProfile   # we'll make sure this exists
from .models import StandSession
from .serializers import StandSessionSerializer

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
    """
    Passenger/dispatcher: give me the next rider from this stand.
    Optional: trusted_only=true
    """
    stand_code = request.data.get('stand_code')
    trusted_only = request.data.get('trusted_only', False)

    if not stand_code:
        return Response({"detail": "stand_code is required"}, status=400)

    try:
        stand = Stand.objects.get(code=stand_code)
    except Stand.DoesNotExist:
        return Response({"detail": "stand not found"}, status=404)

    # base queryset: active sessions at that stand
    qs = StandSession.objects.filter(stand=stand, active=True).order_by('joined_at')

    if trusted_only:
        # filter to sessions whose rider is trusted
        qs = qs.filter(rider__riderprofile__is_trusted=True)

    session = qs.first()
    if not session:
        return Response({"detail": "no available rider"}, status=404)

    # for v1: immediately deactivate them (they got the job)
    session.active = False
    session.save()

    # return rider info
    data = {
        "rider_id": session.rider.id,
        "rider_username": session.rider.username,
        "rider_phone": session.rider.phone,
        "stand": stand.code,
        "trusted": getattr(getattr(session.rider, 'riderprofile', None), 'is_trusted', False)
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
