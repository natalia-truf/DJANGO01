from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings

from shop.api import (
    CategoryViewSet, SupplierViewSet, PointOfSaleViewSet,
    ProductViewSet, ProductImageViewSet, OrderViewSet, ProfileViewSet
)

router = DefaultRouter()
router.register('categories', CategoryViewSet, 'categories')
router.register('suppliers', SupplierViewSet, 'suppliers')
router.register('points', PointOfSaleViewSet, 'points')
router.register('products', ProductViewSet, 'products')
router.register('productimages', ProductImageViewSet, 'productimages')
router.register('orders', OrderViewSet, 'orders')
router.register('profile', ProfileViewSet, 'profile')

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)