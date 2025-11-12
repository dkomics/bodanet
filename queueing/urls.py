from django.urls import path
from . import views

urlpatterns = [
    path('queue/join/', views.join_queue, name='join-queue'),
    path('queue/next/', views.next_rider, name='next-rider'),
    path('queue/complete/', views.complete_trip, name='complete-trip'),
    path('trips/', views.list_trips, name='list-trips'),
]
