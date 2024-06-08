from django.db import models
from accounts.models import CustomUser

class HallStatusChoices(models.TextChoices):
    OPEN = 'Open', 'Open'
    CLOSED = 'Closed', 'Closed'

class HaveChargerChoices(models.TextChoices):
    TRUE = 'true', 'Yes'
    FALSE = 'false', 'No'

class Hall(models.Model):
    status = models.CharField(max_length=6, choices=HallStatusChoices.choices, default=HallStatusChoices.OPEN)
    open_time = models.TimeField()
    close_time = models.TimeField()
    
class Seat(models.Model):
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='seats')
    have_charger = models.CharField(max_length=5, choices=HaveChargerChoices.choices, default=HaveChargerChoices.FALSE)

class Reservation(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE, related_name='reservation')
    start = models.TimeField()
    finish = models.TimeField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        constraint = [
            models.CheckConstraint(
                check=models.Q(start__lt=models.f('finish')),
                name='check_start_before_finish'
            )
        ]

    def save(self, *args, **kwargs):
        overlapping_reservations = Reservation.objects.filter(
            seat=self.seat,
            start__lt=self.finish,
            finish_gt=self.start
        ).exists()
        if overlapping_reservations:
            raise ValueError("This seat is already reserved during the selected time period.")
        super().save(*args, **kwargs)