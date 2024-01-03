from django.urls import path,include
from .views import home_passenger,home_admin
from train_booking.views import search_journey,upcoming_journeys

urlpatterns = [
    path('',upcoming_journeys, name='home'),
    path('home_admin/', home_admin, name='home_admin'),
]