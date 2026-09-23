from rest_framework import serializers
from shop.models import Product, Category, Supplier, PointOfSale, Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'phone']


class PointOfSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointOfSale
        fields = ['id', 'name', 'address']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)          # для чтения (показывает объект)
    category_id = serializers.PrimaryKeyRelatedField(       # для записи (принимает ID)
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    supplier = SupplierSerializer(read_only=True)
    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(),
        source='supplier',
        write_only=True
    )

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category', 'category_id', 'supplier', 'supplier_id', 'description']


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    point = PointOfSaleSerializer(read_only=True)
    point_id = serializers.PrimaryKeyRelatedField(
        queryset=PointOfSale.objects.all(),
        source='point',
        write_only=True
    )

    class Meta:
        model = Order
        fields = ['id', 'product', 'product_id', 'point', 'point_id', 'quantity', 'created_at']