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
        hall = get_object_or_404(self.queryset, pk)
        serializer = HallSerializer(hall)
        return Response(serializer.data)

def get_empty_seats(seat_id):
    seat = Seat.objects.get(id=seat_id)
    hall = seat.hall

    reservations = Reservation.objects.filter(seat=seat).order_by('start')
    empty_times = []
    current_time = datetime.combine(datetime.today(), hall.open_time)
    for reservation in reservations:
        if current_time < reservation.start:
            empty_times.append((current_time, reservation.start))
        current_time = reservation.finish

    close_time = datetime.combine(datetime.today(), hall.close_time)
    if current_time < close_time:
        empty_times.append((current_time, close_time))

    return empty_times

class HallSeatsViewSet(ViewSet):
    queryset = Seat.objects.all()
    
    # get all the seats from all halls
    def list(self, request):
        serializer = SeatSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def list_seats_one_hall(self, request, pk):
        queryset = Seat.objects.filter(hall_id=pk)
        serializer = SeatSerializer(queryset, many=True)
        return Response(serializer.data)
    
    # get all seats from one hall + time they are empty
    @action(detail=True, methods=['get'])
    def empty_times_in_hall(self, request, pk):
        hall = get_object_or_404(Hall, pk=pk)
        seat_ids = Seat.objects.filter(hall=hall).values_list('id', flat=True)
        data = []
        for id in seat_ids:
            empty_times = get_empty_seats(id=id)
            data.append({'seat_id': id, 'empty_times': empty_times})
        return Response(data)
    
    # get empty seats from a hall
    @action(detail=True, methods=['get'])
    def empty_seats_in_hall(self, request, pk):
        hall = get_object_or_404(Hall, pk=pk)
        available_seats = Seat.objects.filter(reservation__isnul=True)
        serializer = SeatSerializer(available_seats, many=True)
        return Response(serializer.data)
    
    # get reserved seats from a hall
    @action(detail=True, methods=['get'])
    def reserved_seats_in_hall(self, request, pk):
        hall = get_object_or_404(Hall, pk=pk)
        reserved_seats = Seat.objects.filter(reservation__isnul=False)
        serializer = SeatSerializer(reserved_seats, many=True)
        return Response(serializer.data)
    
    # get all empty seats in a given time
    @action(detail=True, methods=['get'])
    def empty_seats_in_give_time(self, request):
        start_time = request.query_params.get('start_time', None)
        
        seat = Seat.objects.filter(reservation__finish__lt=start_time)
        if seat:
            serializer = SeatSerializer(seat, many=True)
            return Response(serializer.data)

    # get all empty seats with charger
    @action(detail=True, methods=['get'])
    def empty_seats_with_charger(self, request):
        seats = Seat.objects.filter(have_charger=HaveChargerChoices.TRUE, reservation__isnul=True)
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)
    


class ReservationViewSet(ViewSet):
    @action(detail=True, methods=['post'])
    def reserve_seat(self, request):
        serializer = ReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"message": "the seat reserved successfully"})
    
    def cancel_seat(self, request, pk):
        Reservation.objects.get(pk=pk).delete()
        return Response({"message": "reservation calceled"})




# delete reservation after the time finished






