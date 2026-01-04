from django.shortcuts import render

def finance_overview(request):
    # TODO: Добавить финансовую статистику
    return render(request, 'main/finance/finance.html')
