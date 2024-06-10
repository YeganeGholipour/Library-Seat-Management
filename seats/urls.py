from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import HallViewSet, HallSeatsViewSet, ReservationViewSet

router = DefaultRouter()

router.register(r'halls', HallViewSet, basename='hall')
router.register(r'seats', HallSeatsViewSet, basename='seat')
router.register(r'reservations', ReservationViewSet, basename='reservation')

urlpatterns = [
    path('', include(router.urls)),
]