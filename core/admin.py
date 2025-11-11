# Register your models here.
from django.contrib import admin
from .models import User, Stand
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra', {'fields': ('is_rider', 'phone')}),
    )

admin.site.register(Stand)
