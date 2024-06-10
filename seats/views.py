from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from datetime import datetime
from .models import Hall, Seat, Reservation, HallStatusChoices, HaveChargerChoices
from .serializers import SeatSerializer, HallSerializer, ReservationSerializer

class HallViewSet(ViewSet):
    queryset = Hall.objects.all()

    def list(self, request):
        serializer = HallSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        hall = get_object_or_404(self.queryset, pk=pk)
        serializer = HallSerializer(hall)
        return Response(serializer.data)

def get_empty_seats(seat_id):
    seat = get_object_or_404(Seat, id=seat_id)
    hall = seat.hall

    reservations = Reservation.objects.filter(seat=seat).order_by('start')
    empty_times = []
    current_time = datetime.combine(datetime.today(), hall.open_time)
    for reservation in reservations:
        if current_time.time() < reservation.start:
            empty_times.append((current_time.time(), reservation.start))
        current_time = datetime.combine(datetime.today(), reservation.finish)

    close_time = datetime.combine(datetime.today(), hall.close_time)
    if current_time.time() < close_time.time():
        empty_times.append((current_time.time(), close_time.time()))

    return empty_times

class HallSeatsViewSet(ViewSet):
    queryset = Seat.objects.all()
    
    def list(self, request):
        serializer = SeatSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def list_seats_one_hall(self, request, pk):
        queryset = Seat.objects.filter(hall_id=pk)
        serializer = SeatSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def empty_times_in_hall(self, request, pk):
        hall = get_object_or_404(Hall, pk=pk)
        seat_ids = Seat.objects.filter(hall=hall).values_list('id', flat=True)
        data = []
        for seat_id in seat_ids:
            empty_times = get_empty_seats(seat_id)
            data.append({'seat_id': seat_id, 'empty_times': empty_times})
        return Response(data)
    
    @action(detail=True, methods=['get'])
    def empty_seats_in_hall(self, request, pk):
        hall = get_object_or_404(Hall, pk=pk)
        available_seats = Seat.objects.filter(hall=hall, reservations__isnull=True)
        serializer = SeatSerializer(available_seats, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def reserved_seats_in_hall(self, request, pk):
        hall = get_object_or_404(Hall, pk=pk)
        reserved_seats = Seat.objects.filter(hall=hall, reservations__isnull=False)
        serializer = SeatSerializer(reserved_seats, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def empty_seats_in_given_time(self, request):
        start_time = request.query_params.get('start_time')
        if not start_time:
            return Response({"error": "start_time parameter is required"}, status=400)
        
        seats = Seat.objects.filter(reservations__finish__lt=start_time)
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def empty_seats_with_charger(self, request):
        seats = Seat.objects.filter(have_charger=HaveChargerChoices.TRUE, reservations__isnull=True)
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)

class ReservationViewSet(ViewSet):
    @action(detail=False, methods=['post'])
    def reserve_seat(self, request):
        serializer = ReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "The seat was reserved successfully"})
    
    @action(detail=True, methods=['delete'])
    def cancel_seat(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk)
        reservation.delete()
        return Response({"message": "Reservation cancelled successfully"})


# delete reservation after the time finished
# tasks.py






