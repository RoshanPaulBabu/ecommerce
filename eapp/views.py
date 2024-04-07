from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomerRegistrationForm, LoginForm
from .models import Customer
from django.contrib import messages

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'customer/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            customer = Customer.objects.get(email=email, password=password)
            return redirect('index') 
        except Customer.DoesNotExist:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, 'customer/login.html')
