# urls.py in app_weather

from django.urls import path
from .views import weather_view

urlpatterns = [
    path('weather/', weather_view),
]