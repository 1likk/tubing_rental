from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

class Command(BaseCommand):
    help = 'Создает суперпользователя, если его еще нет'

    def handle(self, *args, **options):
        User = get_user_model()
        
        # Получаем данные из переменных окружения или используем дефолтные
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')
        
        # Проверяем, существует ли уже суперпользователь
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Суперпользователь "{username}" уже существует')
            )
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Суперпользователь "{username}" успешно создан')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Username: {username}')
            )
            self.stdout.write(
                self.style.SUCCESS(f'Password: {password}')
            )
