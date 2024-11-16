from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm

# view function for the homepage
def home_page(request):
    return render(request, 'shop/index.html') 

# view function for the register page
def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user to the database
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login') 
        else:
            messages.error(request, 'Registration failed. Please check the form.')
    else:
        form = RegistrationForm()

    return render(request, 'shop/register.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']

        # Authenticate user using phone number and password
        user = authenticate(request, phone_number=phone_number, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard or homepage
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')

    return render(request, 'shop/login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')