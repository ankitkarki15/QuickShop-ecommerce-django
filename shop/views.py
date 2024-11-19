from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm

# view function for the homepage
def home_page(request):
    return render(request, 'shop/index.html') 


def register_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")  # Add success message
            return redirect('login')  # Ensure 'login' is the correct name in your URLs
        else:
            messages.error(request, "Please correct the errors below.")  # Optional: Add error message
    else:
        form = RegistrationForm()
    
    return render(request, 'shop/register.html', {'form': form})


def login_page(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        password = request.POST['password']

        
        user = authenticate(request, phone_number=phone_number, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')

    return render(request, 'shop/login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')