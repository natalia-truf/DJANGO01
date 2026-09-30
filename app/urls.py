from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers
from shop.api import (
    ProductViewSet, CategoryViewSet, SupplierViewSet,
    PointOfSaleViewSet, OrderViewSet, ProductImageViewSet
)

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'points', PointOfSaleViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'productimages', ProductImageViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)