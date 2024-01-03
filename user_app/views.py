from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login
from .forms import CustomAuthenticationForm,PassengerRegistrationForm,AdminRegistrationForm
from .models import PassegerUser, AdminUser
from train_booking.models import Wallet

def register_passenger(request):
    if request.method == 'POST':
        form = PassengerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PassengerRegistrationForm()
    return render(request, 'user_app/register_passenger.html', {'form': form})

def register_admin(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True
            user.save()
            return redirect('home')
    else:
        form = AdminRegistrationForm()
    return render(request, 'user_app/register_admin.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Check if user is a admin and redirect to admin home page
            if user.role == 'ADMIN':
                
                return redirect('home_admin')
            else:

                try:
                    # Attempt to retrieve the user's wallet
                    wallet = user.wallet
                    wallet_exists = True
                except Wallet.DoesNotExist:
                    # If the wallet does not exist, set wallet_exists to False
                    wallet = None
                    wallet_exists = False
                if not wallet_exists:
                    Wallet.objects.create(user = user)    
                return redirect('home') 
    else:
        form = CustomAuthenticationForm()
    return render(request, 'user_app/login.html', {'form': form})
