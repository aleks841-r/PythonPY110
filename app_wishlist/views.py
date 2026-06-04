from django.shortcuts import render

# Create your views here.

def wishlist_view(request):
    if request.method == "GET":
        # TODO прописать отображение избранного. Путь до HTML - app_wishlist/wishlist.html
        return render(request, 'app_wishlist/wishlist.html')
