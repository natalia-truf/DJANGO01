from django.contrib import admin
from shop.models import Category, Supplier, PointOfSale, Product, Order, ProductImage, Profile


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
    list_display = ['name', 'price', 'category', 'supplier']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'point', 'quantity', 'created_at']
    list_filter = ['user']
    search_fields = ['user__username']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']