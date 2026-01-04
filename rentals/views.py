from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Tubing, RentalSession
import math

def tubing_list(request):
    tubings = Tubing.objects.all().order_by('number')
    
    # Получаем активные сессии и создаем словарь для быстрого доступа
    active_sessions = {}
    for session in RentalSession.objects.filter(status='active').select_related('tubing'):
        active_sessions[session.tubing.id] = session
    
    # Добавляем информацию об активной сессии к каждому тюбингу
    tubings_with_sessions = []
    for tubing in tubings:
        tubing_data = {
            'tubing': tubing,
            'session': active_sessions.get(tubing.id, None)
        }
        tubings_with_sessions.append(tubing_data)
    
    return render(request, 'main/rentals/tubing_list.html', 
                  {'tubings_with_sessions': tubings_with_sessions})


def calculate_rental_price(start_time):
    """Расчет стоимости аренды по секундам"""
    now = timezone.now()
    duration = now - start_time
    total_seconds = duration.total_seconds()
    
    MIN_PRICE = 1000  # Минимальная цена
    SECONDS_IN_HOUR = 3600
    PRICE_PER_SECOND = 0.28  # 0.28 тг за секунду
    
    if total_seconds <= SECONDS_IN_HOUR:
        return MIN_PRICE
    else:
        # Считаем точную сумму за всё время по секундному тарифу
        return math.ceil(total_seconds * PRICE_PER_SECOND)


@require_POST
def start_rental(request, tubing_id):
    """Начать аренду тюбинга"""
    tubing = get_object_or_404(Tubing, id=tubing_id)
    guest_name = request.POST.get('guest_name', '').strip()
    
    if not guest_name:
        return JsonResponse({'success': False, 'error': 'Введите имя гостя'}, status=400)
    
    # Проверяем, что тюбинг свободен
    if tubing.status != 'available':
        return JsonResponse({'success': False, 'error': 'Тюбинг занят'}, status=400)
    
    # Создаем сессию
    session = RentalSession.objects.create(
        tubing=tubing,
        guest_name=guest_name,
        status='active'
    )
    
    # Обновляем статус тюбинга
    tubing.status = 'busy'
    tubing.save()
    
    return JsonResponse({
        'success': True,
        'session_id': session.id,
        'start_time': session.start_time.isoformat()
    })


@require_POST
def end_rental(request, session_id):
    """Завершить аренду и рассчитать сумму"""
    session = get_object_or_404(RentalSession, id=session_id, status='active')
    
    # Рассчитываем стоимость
    final_cost = calculate_rental_price(session.start_time)
    
    # Обновляем сессию
    session.end_time = timezone.now()
    session.final_cost = final_cost
    session.status = 'completed'
    session.save()
    
    # Освобождаем тюбинг
    tubing = session.tubing
    tubing.status = 'available'
    tubing.save()
    
    # Вычисляем время аренды
    duration = session.end_time - session.start_time
    total_seconds = int(duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    
    return JsonResponse({
        'success': True,
        'final_cost': float(final_cost),
        'duration': {
            'hours': hours,
            'minutes': minutes,
            'seconds': seconds,
            'total_seconds': total_seconds
        }
    })
