from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse, JsonResponse
from .models import DATABASE

# Create your views here.

def product_view_json(request):
    if request.method == "GET":
        data = DATABASE
        # TODO Вернуть JsonResponse с объектом DATABASE и параметрами отступов и кодировок,
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})
        # как в приложении app_weather

def shop_view(request):
    if request.method == "GET":
        with open('app_store/shop.html', encoding="utf-8") as f:
            data = f.read()  # Читаем HTML файл
        return HttpResponse(data)  # Отправляем HTML файл как ответ