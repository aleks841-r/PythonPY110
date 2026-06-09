from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Системные маршруты
    path('admin/', admin.site.urls),

    # Маршруты приложений (Делегирование)
    #path('datetime/', include('app_datetime.urls')),  # Перенесли datetime и dynamic_datetime сюда
    #path('random/', include('app_random.urls')),      # Создали отдельное приложение под random
    path('weather/', include('app_weather.urls')),    # Добавили префикс 'weather/' для чистоты URL
    path('wishlist/', include('app_wishlist.urls')),

    # Главная страница и магазин
    path('', include('app_store.urls')),              # Оставляем пустой префикс для главной страницы
    path('login/', include('app_login.urls')),
]
