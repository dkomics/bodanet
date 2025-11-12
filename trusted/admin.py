from django.contrib import admin
from .models import RiderProfile


@admin.register(RiderProfile)
class RiderProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'stand', 'is_trusted', 'plate_number')
    list_filter = ('is_trusted', 'stand')
    search_fields = ('user__username', 'user__phone', 'plate_number')