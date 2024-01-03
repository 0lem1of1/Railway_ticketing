from django.urls import path
from .views import register_passenger,register_admin,user_login

urlpatterns = [
    path('register/', register_passenger, name='register'),
    path('register-admin/', register_admin, name='register-admin'),
    path('login/', user_login, name='user_login'),
]