from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home_passenger(request):
    return render(request, 'main/home_passenger.html')

@login_required(login_url='login')
def home_admin(request):
    # Check if the logged-in user has the role "ADMIN"
    if request.user.role == 'ADMIN':
        return render(request, 'main/home_admin.html')
    else:
        # Redirect to a different page or show an error message
        return render(request, 'access_denied.html')