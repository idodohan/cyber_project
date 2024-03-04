from django.shortcuts import render, redirect
from .forms import CustomerForm
from .models import Customer


def dashboard(request):
    customers = Customer.objects.all()
    return render(request, 'dashboard.html',  {'customers': customers})


def add_customer(request):
    if request.method == 'POST':
        '''
        ___Customer.objects.raw(request.text())___ -> this is not exactly correct. it needs to build  a sql query from requst.POST. youll figure it out

        request.text() can be good; "ADD Customer email:viktor@blal, name:vik" -> adds a new customer
                but can also be bad; "DELETE *"                                -> deletes a customer
        
        this occurs because the query is passed as 'raw' and we can send a query as an argument of the request
        
        the way to fix the vulnerability is to 'parametize' the query in this manner:
        
        ___CustomerForm(request.POST)___
        Explanation:
        the request now MUST recieve the following parameters: (email: str, name: str)
        thus we are unable to pass a query 'as is'
        '''

        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = CustomerForm()

    return render(request, 'add_customer.html', {'form': form})
