from django.db import models
from django.utils import timezone

class Tubing(models.Model):
    # Статусы тюбинга
    STATUS_CHOISES = [
        ('available', 'Бос'),
        ('busy', 'Бос емес'),
        ('broken', 'Жөндеуде')
    ]

    number = models.PositiveIntegerField(unique=True, verbose_name="Тюбинг номер")
    status = models.CharField(max_length=20, choices=STATUS_CHOISES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Тюбинг № {self.number} ({self.get_status_display()})"
    
    class Meta:
        verbose_name = "Тюбинг"
        verbose_name_plural = "Тюбинги"


class RentalSession(models.Model):
    STATUS_CHOICES = [
        ('active', 'Активна'),
        ('completed', 'Завершена'),
    ]
    
    tubing = models.ForeignKey(Tubing, on_delete=models.PROTECT, verbose_name="Тюбинг")
    guest_name = models.CharField(max_length=100, verbose_name="Имя гостя")
    phone_number = models.CharField(max_length=20, verbose_name="Номер телефона", blank=True, default="")
    start_time = models.DateTimeField(auto_now_add=True, verbose_name="Время начала")
    end_time = models.DateTimeField(null=True, blank=True, verbose_name="Время окончания")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Статус")
    final_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Итоговая сумма")
    
    def __str__(self):
        return f"{self.guest_name} - Тюбинг №{self.tubing.number}"
    
    class Meta:
        verbose_name = "Сессия аренды"
        verbose_name_plural = "Сессии аренды"
        ordering = ['-start_time']
