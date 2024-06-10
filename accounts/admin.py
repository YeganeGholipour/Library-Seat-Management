from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'username', 'password', 'email', 'first_name', 'last_name']
