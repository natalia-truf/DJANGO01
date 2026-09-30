from rest_framework import viewsets
from shop.models import Product, Category, Supplier, PointOfSale, Order, ProductImage
from shop.serializers import (
    ProductSerializer, CategorySerializer, SupplierSerializer,
    PointOfSaleSerializer, OrderSerializer, ProductImageSerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class PointOfSaleViewSet(viewsets.ModelViewSet):
    queryset = PointOfSale.objects.all()
    serializer_class = PointOfSaleSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer