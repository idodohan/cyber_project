from django.shortcuts import render, redirect
from .forms import CustomerForm
from .models import Customer


def dashboard(request):
    customers = Customer.objects.all()
    return render(request, 'dashboard.html',  {'customers': customers})


def add_customer(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CustomerForm()

    return render(request, 'add_customer.html', {'form': form})
