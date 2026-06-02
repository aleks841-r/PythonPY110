# urls.py in app_store

from django.urls import path
from .views import product_view_json, shop_view

urlpatterns = [
    path('product/', product_view_json),
    path('', shop_view),
]