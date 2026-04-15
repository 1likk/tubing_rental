from django.shortcuts import render
from rentals.models import Tubing, RentalSession
from django.db.models import Sum
from django.utils import timezone
from datetime import datetime

def dashboard(request):
    active_rentals_count = RentalSession.objects.filter(status="active").count()

    total_tubings = Tubing.objects.count()
    available_tubings = Tubing.objects.filter(status="available").count()
    inventory_stats = f"{available_tubings} / {total_tubings}"

    today = timezone.now().date()
    today_revenue_data = RentalSession.objects.filter(
        status="completed",
        end_time__date=today
    ).aggregate(total=Sum('final_cost'))
    today_revenue = today_revenue_data['total'] or 0

    
    current_month = timezone.now().month
    current_year = timezone.now().year
    month_revenue_data = RentalSession.objects.filter(
        status="completed",
        end_time__month=current_month,
        end_time__year=current_year
    ).aggregate(total=Sum('final_cost'))
    month_revenue = month_revenue_data['total'] or 0

    latest_rentals = RentalSession.objects.all().order_by('-start_time')[:5]

    context = {
        'active_count': active_rentals_count,
        'inventory_stats': inventory_stats,
        'today_revenue': today_revenue,
        'month_revenue': month_revenue,
        'latest_rentals': latest_rentals
    }

    return render(request, 'main/index/index.html', context)

