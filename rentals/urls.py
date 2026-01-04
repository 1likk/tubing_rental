from django.urls import path 
from . import views


app_name = 'rentals'

urlpatterns = [
    path('', views.tubing_list, name='rental_list'),
    path('tubings/', views.tubing_list, name='tubing_list'),
    path('start/<int:tubing_id>/', views.start_rental, name='start_rental'),
    path('end/<int:session_id>/', views.end_rental, name='end_rental'),
]