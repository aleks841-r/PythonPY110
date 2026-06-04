from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotFound
from django.http import HttpResponse, JsonResponse
from .models import DATABASE
from logic.services import filtering_category
from logic.control_cart import view_in_cart, add_to_cart, remove_from_cart

# Create your views here.

def product_view_json(request):
    if request.method == "GET":
        # Обработка id из параметров запроса (уже было реализовано ранее)
        id_ = request.GET.get('id')
        if id_:
            if id_ in DATABASE:
                return JsonResponse(DATABASE[id_], json_dumps_params={'ensure_ascii': False, 'indent': 4})
            return HttpResponseNotFound("Данного продукта нет в базе данных")

        # Обработка фильтрации из параметров запроса
        category_key = request.GET.get("category")  # Считали 'category'
        if ordering_key := request.GET.get("ordering"): # Если в параметрах есть 'ordering'
            reverse = request.GET.get("reverse")
            if reverse and reverse.lower() == 'true':  # Если в параметрах есть 'ordering' и 'reverse'=True
                #  TODO Использовать filtering_category и провести фильтрацию с параметрами category, ordering, reverse=True
                data = filtering_category(database=DATABASE, category_key=category_key,ordering_key=ordering_key,reverse=True)
            else:  # Если не обнаружили в адресно строке ...&reverse=true , значит reverse=False
                #  TODO Использовать filtering_category и провести фильтрацию с параметрами category, ordering, reverse=False
                data = filtering_category(database=DATABASE, category_key=category_key,ordering_key=ordering_key,reverse=False)
        else:
            #  TODO Использовать filtering_category и провести фильтрацию с параметрами category
            data = filtering_category(database=DATABASE, category_key=category_key)
        # В этот раз добавляем параметр safe=False, для корректного отображения списка в JSON
        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})

#def shop_view(request):
#    if request.method == "GET":
#        with open('app_store/shop.html', encoding="utf-8") as f:
#            data = f.read()  # Читаем HTML файл
#        return HttpResponse(data)  # Отправляем HTML файл как ответ

def shop_view(request):
    if request.method == "GET":
        return render(request, 'app_store/shop.html', context={"products": DATABASE.values()})

def cart_view(request):
    if request.method == "GET":
        username = 'Vasya'
        data = view_in_cart(username)[username]  # Получаем корзину пользователя username

        products = []  # Список продуктов
        for product_id, quantity in data['products'].items():
            product = DATABASE[product_id]  # Получаем информацию о продукте
            # TODO в словарь product под ключом "quantity" запишите текущее значение количества товара в корзине
            product["quantity"] = quantity # Реализуйте
            # TODO в словарь product под ключом "price_total" посчитайте и запишите общую стоимость товара как произведение
            #  его количества в корзине на цену с учетом скидки ('price_after'). Значение цены "price_total" приведите к формату
            #  2 символов после запятой
            product["price_total"] = round((quantity * product["price_after"]), 2)  # Реализуйте
            # TODO добавьте словарь product в конец списка products
            products.append(product)
            # Реализуйте

        return render(request, "app_store/cart.html", context={"products": products})

def product_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):  # Проверяем, что в параметр page передали значение строкового типа
            for data in DATABASE.values():  # Перебираем все товары (словари) в DATABASE
                if data['html'] == page:  # Если значение переданного параметра совпадает именем html файла, получаемого по ключу
                    # TODO 1. Откройте файл open(f'app_store/product/{page}.html', encoding="utf-8") (Не забываем про контекстный менеджер with)
                    # TODO 2. Прочитайте его содержимое
                    with open(f'app_store/product/{page}.html', encoding="utf-8") as f:
                        # TODO 3. Верните HttpResponse c содержимым html файла
                        return HttpResponse(f.read())

        elif isinstance(page, int): # Ветка для обработки типа int
            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
            if data:  # Если по данному page было найдено значение
                with open(f'app_store/product/{data["html"]}.html', encoding="utf-8") as f: # Определяем название файла для открытия
                    return HttpResponse(f.read())

            return HttpResponse(status=404)

def cart_view_json(request):
    if request.method == "GET":
        username = ''
        # TODO Вызвать ответственную за это действие функцию view_in_cart(username)
        data = view_in_cart(username)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False, 'indent': 4})

def cart_add_view_json(request, id_product):
    if request.method == "GET":
        username = 'Vasya'
        # TODO Вызвать ответственную за это действие функцию add_to_cart(id_product, username)
        result = add_to_cart(id_product, username)
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в корзину"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное добавление в корзину"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})

def cart_del_view_json(request, id_product):
    if request.method == "GET":
        username = 'Vasya'
        # TODO Вызвать ответственную за это действие функцию remove_from_cart(id_product, username)
        result = remove_from_cart(id_product, username)
        if result:
            return JsonResponse({"answer": "Продукт успешно удалён из корзины"},
                                json_dumps_params={'ensure_ascii': False})

        return JsonResponse({"answer": "Неудачное удаление из корзины"},
                            status=404,
                            json_dumps_params={'ensure_ascii': False})