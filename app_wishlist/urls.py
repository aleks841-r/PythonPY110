from django.urls import path
from .views import wishlist_view
#  TODO Импортируйте ваше представление

app_name = 'app_wishlist'

urlpatterns = [
    path('', wishlist_view, name=app_name),  # TODO Зарегистрируйте обработчик
]