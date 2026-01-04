from django.shortcuts import render
from rentals.models import Tubing
from rentals.models import RentalSession
from django.db.models import Sum
from django.utils import timezone

def dashboard(request):
    
    return render(request, 'main/index/index.html')

