from django.contrib import admin
from .models import StandSession

@admin.register(StandSession)
class StandSessionAdmin(admin.ModelAdmin):
    list_display = ('rider', 'stand', 'joined_at', 'active')
    list_filter = ('stand', 'active')
    search_fields = ('rider__username', 'stand__name', 'stand__code')
    ordering = ('-joined_at',)
