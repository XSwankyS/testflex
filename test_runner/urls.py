from django.contrib import admin
from django.urls import path, include  # добавляем include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('scenarios.urls')),  # добавляем маршруты для вашего приложения
]
