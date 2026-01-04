from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),
    path('rentals/', include('rentals.urls', namespace='rentals')),
    path('finance/', include('finance.urls', namespace='finance')),
]
