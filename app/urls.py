from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from shop.api import (
    ProductViewSet, CategoryViewSet, SupplierViewSet,
    PointOfSaleViewSet, OrderViewSet
)

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'points', PointOfSaleViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]