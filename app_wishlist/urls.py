from django.urls import path
from .views import (
    wishlist_view,
    wishlist_add_view,
    wishlist_remove_view,
    wishlist_view_json,
    wishlist_add_view_json,
    wishlist_del_view_json,
)

app_name = 'app_wishlist'

urlpatterns = [
    path('', wishlist_view, name='wishlist_view'),
    path('add/<str:id_product>', wishlist_add_view, name='wishlist_add'),
    path('remove/<str:id_product>', wishlist_remove_view, name="wishlist_remove"),
    path('api/', wishlist_view_json),
    path('api/add/<id_product>', wishlist_add_view_json),
    path('api/del/<id_product>', wishlist_del_view_json),
]