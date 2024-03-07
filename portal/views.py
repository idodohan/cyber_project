from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CustomerForm
from .models import Customer


def dashboard(request):
    customers = Customer.objects.all()
    return render(request, 'dashboard.html',  {'customers': customers})


def add_customer(request):
    if request.method == 'POST':
        name = request.POST.get('username', '')
        email = request.POST.get('email', '')

        # Basic input validation (you should customize this based on your requirements)
        if not name or not email:
            return render(request, 'add_customer.html')

        else:
            # Save data to the database using raw SQL query
            with connection.cursor() as cursor:
                cursor.executescript("INSERT INTO portal_customer VALUES (NULL, "+name+", '"+email+"')")
        return redirect('dashboard')
    return render(request, 'add_customer.html')
