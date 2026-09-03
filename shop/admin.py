from django.contrib import admin
from shop.models import Category, Product, Size, Season, Supplier

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    pass

@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    pass

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    pass

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'size', 'season', 'supplier', 'color', 'stock']