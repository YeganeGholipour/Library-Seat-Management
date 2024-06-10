# tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Reservation

@shared_task
def delete_expired_reservations():
    now = timezone.now()
    expired_reservations = Reservation.objects.filter(finish__lt=now)
    expired_reservations.delete()
