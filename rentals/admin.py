from django.contrib import admin
from .models import Tubing, RentalSession

@admin.register(Tubing)
class TubingAdmin(admin.ModelAdmin):
    list_display = ('number', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('number',)
    ordering = ('number',)

@admin.register(RentalSession)
class RentalSessionAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'phone_number', 'tubing', 'start_time', 'end_time', 'status', 'final_cost')
    list_filter = ('status', 'start_time')
    search_fields = ('guest_name', 'phone_number', 'tubing__number')
    ordering = ('-start_time',)
