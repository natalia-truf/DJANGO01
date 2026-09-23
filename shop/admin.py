from django.contrib import admin
from shop.models import Category, Supplier, PointOfSale, Product, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    pass

@admin.register(PointOfSale)
class PointOfSaleAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'supplier', 'point', 'description']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'quantity', 'created_at']