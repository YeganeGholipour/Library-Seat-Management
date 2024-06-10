from django.contrib import admin
from .models import Hall, Seat, Reservation

@admin.register(Hall)
class UserAdmin(admin.ModelAdmin):
    list_display = ['status', 'open_time', 'close_time']

@admin.register(Seat)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['hall', 'have_charger']

@admin.register(Reservation)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['seat', 'start', 'finish', 'user']


