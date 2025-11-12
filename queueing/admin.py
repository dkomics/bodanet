from django.contrib import admin
from .models import StandSession, Trip

@admin.register(StandSession)
class StandSessionAdmin(admin.ModelAdmin):
    list_display = ('rider', 'stand', 'joined_at', 'active')
    list_filter = ('stand', 'active')
    search_fields = ('rider__username', 'stand__name', 'stand__code')
    ordering = ('-joined_at',)

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('rider', 'stand', 'destination_stand', 'destination_text', 'requested_at', 'trusted_only')
    list_filter = ('stand', 'destination_stand', 'trusted_only')
    search_fields = ('rider__username', 'stand__name', 'stand__code', 'destination_text')
    ordering = ('-requested_at',)
