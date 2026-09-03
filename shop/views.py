from django.shortcuts import render
from django.views import View
from shop.models import Product

class ShowProductsView(View):
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        return render(request, 'shop/show_shop.html', {'products': products})