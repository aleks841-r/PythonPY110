from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotFound
from django.shortcuts import render
from django.shortcuts import redirect

from app_store.models import DATABASE
from logic.control_wishlist import view_in_wishlist, add_to_wishlist, remove_from_wishlist


@login_required(login_url='app_login:login_view')
def wishlist_view(request):
    if request.method == "GET":
        username = get_user(request).username
        data = view_in_wishlist(username)[username]  # Получаем избранное для пользователя username

        products = []  # Список продуктов
        for product_id in data['products']:
            if product_id in DATABASE:
                product_info = DATABASE[product_id] # Получаем информацию о конкретном продукте (это словарь)
                product_info['id'] = product_id # Добавляем идентификатор продукта
                products.append(product_info) # Создаем список словарей избранных продуктов

        return render(request, "app_wishlist/wishlist.html", context={"products": products})


@login_required(login_url='app_login:login_view')
def wishlist_add_view(request, id_product):
    if request.method == "GET":
        username = get_user(request).username
        result = add_to_wishlist(id_product, username)
        if result:
            return redirect("app_wishlist:wishlist_view")

    return HttpResponseNotFound("Неудачное добавление в корзину")
