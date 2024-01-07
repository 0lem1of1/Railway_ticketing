from django.urls import path
from .views import search_journey,add_train,search_results,create_booking,success_page,wallet_interface,bookings,train_list,update_train,delete_train,cancel_booking,edit_passenger,export_bookings_excel

urlpatterns = [

    path('search/', search_journey, name='search_trains'),
    path('search_results/', search_results, name='search_results'),
    path('create_booking/', create_booking, name='create_booking'),
    path('success_page/', success_page, name='success_page'),
    path('wallet_interface/', wallet_interface, name='wallet_interface'),
    path('add_train/', add_train, name='add_train'),
    path('train_list/', train_list, name='train_list'),
    path('update_train/<int:train_id>/', update_train, name='update_train'),
    path('delete_train/<int:train_id>/', delete_train, name='delete_train'),    
    path('bookings/<int:train_id>/', bookings, name='bookings'),
    path('cancel_booking/<int:booking_id>/', cancel_booking, name='cancel_booking'),
    path('edit_passenger/<int:passenger_id>/', edit_passenger, name='edit_passenger'),
    path('export_bookings_excel/<int:train_id>/', export_bookings_excel, name='export_bookings_excel'),





    



]