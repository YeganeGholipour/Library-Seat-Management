from rest_framework import serializers
from .models import Hall, Seat, Reservation
from accounts.models import CustomUser

class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = '__all__'

class HallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    seat = serializers.PrimaryKeyRelatedField(queryset=Seat.objects.all())
    class Meta:
        model = Reservation
        fields = ['seat', 'start', 'finish']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user

        reservation = Reservation.objects.create(**validated_data)
        reservation.save()
        return reservation



