# marketplace_core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('marketplace_app.urls')),  # Подключаем маршруты приложения
]
