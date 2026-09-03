from rest_framework import serializers
from shop.models import Product, Category, Size, Season, Supplier

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = ['id', 'name']

class SeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = ['id', 'name']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'phone']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    size = SizeSerializer(read_only=True)
    season = SeasonSerializer(read_only=True)
    supplier = SupplierSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category', 'size', 'season', 'supplier', 'description', 'color', 'stock']