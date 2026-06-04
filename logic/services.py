def filtering_category(database: dict[str, dict],
                       category_key: [None, str] = None,
                       ordering_key: [None, str] = None,
                       reverse: bool = False):
    """
    Функция фильтрации данных по параметрам

    :param database: База данных товаров. (словарь словарей. При проверке в качестве database будет передаваться словарь DATABASE из models.py)
    :param category_key: [Опционально] Ключ для группировки категории. Если нет ключа, то рассматриваются все товары.
    :param ordering_key: [Опционально] Ключ по которому будет произведена сортировка результата.
    :param reverse: [Опционально] Выбор направления сортировки:
        False - сортировка по возрастанию;
        True - сортировка по убыванию.
    :return: list[dict] список товаров с их характеристиками, попавших под условия фильтрации. Если нет таких элементов,
    то возвращается пустой список
    """
    categories = {item['category'] for item in database.values() if 'category' in item}
    one_category = category_key is not None and category_key in categories
    if one_category:
        # TODO При помощи фильтрации в list comprehension профильтруйте товары по категории (ключ 'category') в продукте database. Или можете использовать
        # обычный цикл или функцию filter. Допустим фильтрацию в list comprehension можно сделать по следующему шаблону
        # [product for product in database.values() if ...] подумать, что за фильтрующее условие можно применить.
        # Сравните значение категории продукта со значением category_key
        # Фильтрация:
        step1 = {
            product_id: product
            for product_id, product in database.items()
            if product.get('category') == category_key
        }
        # Преобразование в список:
        result = [{**product, 'id': product_id} for product_id, product in step1.items()]
    else:
        # TODO Трансформируйте словарь словарей database в список словарей
        # В итоге должен быть [dict, dict, dict, ...], где dict - словарь продукта из database
        # Фильтрация:
        step1 = {
            cat: {
                product_id: product
                for product_id, product in database.items()
                if product.get('category') == cat
                }
            for cat in categories
        }
        # Преобразование в список словарей:
        result = {
            cat: [{**product, 'id': product_id} for product_id, product in products_dict.items()]
            for cat, products_dict in step1.items()
        }
    if ordering_key is not None:
        # TODO Проведите сортировку result по ordering_key и параметру reverse
        # Так как result будет списком, то можно применить метод sort, но нужно определиться с тем по какому элементу сортируем и в каком направлении
        # result.sort(key=lambda ..., reverse=reverse)
        # Вспомните как можно сортировать по значениям словаря при помощи lambda функции
        sort_func = lambda x: x.get(ordering_key, 0)
        if one_category:
            result.sort(key=sort_func, reverse=reverse)
        else:
            for cat_list in result.values():
                cat_list.sort(key=sort_func, reverse=reverse)
    return result


if __name__ == "__main__":
    from app_store.models import DATABASE

    test = [
        {'name': 'Клубника', 'discount': None, 'price_before': 500.0,
         'price_after': 500.0,
         'description': 'Сладкая и ароматная клубника, полная витаминов, чтобы сделать ваш день ярче.',
         'rating': 5.0, 'review': 200, 'sold_value': 700,
         'weight_in_stock': 400,
         'category': 'Фрукты', 'id': 2, 'url': 'app_store/images/product-2.jpg',
         'html': 'strawberry'},

        {'name': 'Яблоки', 'discount': None, 'price_before': 130.0,
         'price_after': 130.0,
         'description': 'Сочные и сладкие яблоки - идеальная закуска для здорового перекуса.',
         'rating': 4.7, 'review': 30, 'sold_value': 70, 'weight_in_stock': 200,
         'category': 'Фрукты2', 'id': 10, 'url': 'app_store/images/product-10.jpg',
         'html': 'apple'}
    ]
    # Проверяем корректность выполнения функции
    print('Проверка фильтрации: ', filtering_category(DATABASE, 'Фрукты', 'price_after', True) == test)  # True
