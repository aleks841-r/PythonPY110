import json
import os
from app_store.models import DATABASE

PATH_WISHLIST = 'wishlist.json'  # Путь до файла с избранным


def view_in_wishlist(username: str = '') -> dict:
    """
    Просматривает файл избранного: wishlist.json, если пользователя с именем username нет, то создает его в файле

    :param username: Имя пользователя

    :return: Содержимое 'wishlist.json'
    """
    empty_user_wishlist = {'products': []}  # У пользователя нет избранного

    if os.path.exists(PATH_WISHLIST):  # Если файл с избранным существует
        with open(PATH_WISHLIST, encoding='utf-8') as f:  # Открываем файл
            wishlist = json.load(f)  # Считываем файл
            if username not in wishlist:  # Если у пользователя нет избранного, то создаем запись с пустым избранным для него
                wishlist[username] = empty_user_wishlist
    else:  # Если файла с избранным нет, создаем файл и создаем запись с пустым избранным для пользователя
        wishlist = {username: empty_user_wishlist}

    with open(PATH_WISHLIST, mode='w', encoding='utf-8') as f:  # Создаём файл и записываем избранное
        json.dump(wishlist, f)

    return wishlist  # Возвращаем содержимое избранного (все пользователи)


def add_to_wishlist(id_product: str, username: str = '') -> bool:
    """
    Добавляет продукт в избранное, если в избранном нет данного продукта

    :param id_product: Идентификационный номер продукта в виде строки
    :param username: Имя пользователя

    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления
    """
    # Проверяем, существует ли добавляемый продукт с id_product в базе данных DATABASE
    if id_product not in DATABASE:
        return False

    user_wishlist = view_in_wishlist(username) # Просматриваем файл избранного (функция view_in_wishlist)
    products_list = user_wishlist[username]["products"] # Составляем список продуктов из избранного

    # Если продукт уже присутствует в избранном
    if id_product in products_list:
        return False

    # Иначе, добавляем продукт в избранное и сохраняем файл
    products_list.append(id_product)
    with open(PATH_WISHLIST, "w", encoding="utf-8") as f:
        json.dump(user_wishlist, f, ensure_ascii=False, indent=4)

    return True


def remove_from_wishlist(id_product: str, username: str = '') -> bool:
    """
    Удаляет продукт из избранного

    :param id_product: Идентификационный номер продукта в виде строки.
    :param username: Имя пользователя

    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления
    """
    # Проверяем, существует ли добавляемый продукт с id_product в базе данных DATABASE
    if id_product not in DATABASE:
        return False

    user_wishlist = view_in_wishlist(username) # Просматриваем файл избранного (функция view_in_wishlist)
    products_list = user_wishlist[username]["products"] # Составляем список продуктов из избранного

    # Если продукт не присутствует в избранном
    if id_product not in products_list:
        return False

    # Иначе, удаляем продукт в избранное и сохраняем файл
    products_list.remove(id_product)
    with open(PATH_WISHLIST, "w", encoding="utf-8") as f:
        json.dump(user_wishlist, f, ensure_ascii=False, indent=4)

    return True


if __name__ == "__main__":
    while True:
        try:
            print("\n=============================================")
            print("1. view_in_wishlist(username)")
            print("2. add_to_wishlist(id_product, username)")
            print("3. remove_from_wishlist(id_product, username)")
            print("0. exit")
            print("=============================================")

            choice = input("[!!!] Выберите действие: ").strip()

            if choice == "1":
                test_user = input("[!!!] Введите 'username': ").strip()
                result = view_in_wishlist(test_user)
                print(f"===> Результат выполнения функции: {result}")

            elif choice == "2":
                print("[!!!] Доступные 'id_product': ", list(DATABASE.keys()))
                prod = input("[!!!] Введите 'id_product': ").strip()

                print("Доступные 'username': ", list(view_in_wishlist()))
                user = input("Введите 'username': ").strip()

                result = add_to_wishlist(id_product=prod, username=user)
                print(f"===> Результат выполнения функции: {result}")

            elif choice == "3":
                print("[!!!] Доступные 'id_product': ", list(DATABASE.keys()))
                prod = input("[!!!] Введите 'id_product': ").strip()

                print("Доступные 'username': ", list(view_in_wishlist()))
                user = input("Введите 'username': ").strip()

                result = remove_from_wishlist(id_product=prod, username=user)
                print(f"===> Результат выполнения функции: {result}")

            elif choice == "0":
                print("Выход...")
                break

            else:
                print("[!!!] Ошибка: Неверный пункт меню.")

        except KeyboardInterrupt:
            print("Выход...")
            break