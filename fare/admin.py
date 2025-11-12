from django.contrib import admin
from .models import FareRule

@admin.register(FareRule)
class FareRuleAdmin(admin.ModelAdmin):
    list_display = ('origin', 'destination', 'recommended_fare', 'min_fare', 'max_fare', 'updated_at')
    list_filter = ('origin', 'destination')
    search_fields = ('origin__name', 'origin__code', 'destination__name', 'destination__code')
