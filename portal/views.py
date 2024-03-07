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

        if not name or not email:
            return render(request, 'add_customer.html')

        else:
            with connection.cursor() as cursor:
                cursor.executescript("insert into portal_customer(name, email) values('{0}', '{1}')".format(name, email))
        return redirect('dashboard')
    return render(request, 'add_customer.html')
