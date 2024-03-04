from . import views
from django.urls import path, include

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_customer/', views.add_customer, name='add_customer')
]