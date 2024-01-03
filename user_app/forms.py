from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django import forms
from user_app.models import User,PassegerUser,AdminUser  # Update with the correct import path

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User


class PassengerRegistrationForm(UserCreationForm):
    class Meta:
        model = PassegerUser
        fields = ['username', 'password1', 'password2']

class AdminRegistrationForm(UserCreationForm):
    class Meta:
        model = AdminUser
        fields = ['username', 'password1', 'password2']