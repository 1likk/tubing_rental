from django.shortcuts import render
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncDate
from django.utils import timezone
from rentals.models import RentalSession 
from datetime import timedelta, datetime


def finance_overview(request):
    completed_rentals = RentalSession.objects.filter(status='completed')
    
    stats = completed_rentals.aggregate(
        total_revenue=Sum('final_cost'),
        total_count=Count('id'),
        avg_check=Avg('final_cost')
    )
    
    last_week = timezone.now() - timedelta(days=7)
    daily_data = (
        completed_rentals.filter(end_time__gte=last_week)
        .annotate(day=TruncDate('end_time'))
        .values('day')
        .annotate(revenue=Sum('final_cost'))
        .order_by('day')   
    )

    labels = [item['day'].strftime('%d %b') if item['day'] else '' for item in daily_data]
    chart_values = [float(item['revenue']) if item['revenue'] else 0 for item in daily_data]

    context = {
        'total_revenue': stats['total_revenue'] or 0,
        'total_count': stats['total_count'] or 0,
        'avg_check': round(stats['avg_check'] or 0) if stats['avg_check'] else 0,
        'labels': labels,
        'chart_data': chart_values
    }

    
    return render(request, 'main/finance/finance.html', context)

