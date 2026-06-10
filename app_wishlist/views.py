from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render, redirect

from app_store.models import DATABASE
from logic.control_wishlist import view_in_wishlist, add_to_wishlist, remove_from_wishlist


@login_required(login_url='app_login:login_view')
def wishlist_view(request):
    """
    Просмотр всех продуктов в избранном у пользователя
    """
    if request.method == "GET":
        username = get_user(request).username
        data = view_in_wishlist(username)[username] # Получаем избранное для пользователя username

        products = []  # Список продуктов
        for product_id in data['products']:
            if product_id in DATABASE:
                product_info = DATABASE[product_id] # Получаем информацию о конкретном продукте (это словарь)
                product_info['id'] = product_id # Добавляем идентификатор продукта
                products.append(product_info) # Создаем список словарей избранных продуктов

        # Передать HTML-страницу с сервере
        return render(request, "app_wishlist/wishlist.html", context={"products": products})


@login_required(login_url='app_login:login_view')
def wishlist_add_view(request, id_product):
    """
    Добавление нового продукта в избранное у пользователя
    """
    if request.method == "GET":
        username = get_user(request).username
        result = add_to_wishlist(id_product, username) # Добавляем новый продукт в избранное
        if result:
            # Перенаправляем на именованный маршрут списка избранного
            return redirect("app_wishlist:wishlist_view")

    return HttpResponseNotFound("Неудачное добавление в избранное")


@login_required(login_url='app_login:login_view')
def wishlist_remove_view(request, id_product):
    """
    Удаление продукта из избранного у пользователя
    """
    if request.method == "GET":
        username = get_user(request).username
        result = remove_from_wishlist(id_product, username) # Удаляем продукт из избранного
        if result:
            # Перенаправляем на именованный маршрут списка избранного
            return redirect("app_wishlist:wishlist_view")

    return HttpResponseNotFound("Неудачное удаление из избранного")


@login_required(login_url='app_login:login_view')
def wishlist_view_json(request):
    """
    Просмотр всех продуктов в избранном для пользователя и возвращение этого в JSON
    """
    if request.method == "GET":
        username = get_user(request).username
        data = view_in_wishlist(username)[username] # Получаем избранное для пользователя username
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})


@login_required(login_url='app_login:login_view')
def wishlist_add_view_json(request, id_product: str):
    """
    Добавление продукта в избранное и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        username = get_user(request).username
        result = add_to_wishlist(id_product, username)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в избранное"})

        return JsonResponse({"answer": "Неудачное добавление в избранное"}, status=404)


@login_required(login_url='app_login:login_view')
def wishlist_del_view_json(request, id_product: str):
    """
    Удаление продукта из избранного и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        username = get_user(request).username
        result = remove_from_wishlist(id_product, username)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из избранного"})

        return JsonResponse({"answer": "Неудачное удаление из избранного"}, status=404)