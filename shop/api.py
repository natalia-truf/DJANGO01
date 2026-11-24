from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from django.db.models import F

from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count, Sum, Avg, Max, Min

from shop.models import Product, Category, Supplier, PointOfSale, Order, ProductImage, Profile
from shop.serializers import (
    ProductSerializer, CategorySerializer, SupplierSerializer,
    PointOfSaleSerializer, OrderSerializer, ProductImageSerializer, ProfileSerializer
)


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 10000


class ProductStatsSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    avg_price = serializers.FloatField()
    max_price = serializers.FloatField()
    min_price = serializers.FloatField()


class OrderStatsSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    total_items = serializers.IntegerField()
    total_sum = serializers.DecimalField(max_digits=12, decimal_places=2)


class CountStatsSerializer(serializers.Serializer):
    count = serializers.IntegerField()


def is_admin_or_seller(user):
    if user.is_superuser:
        return True
    if hasattr(user, 'profile') and user.profile.role in ['admin', 'seller']:
        return True
    return False


class CategoryViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None

    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            qs = qs.filter(name__icontains=name)
        return qs

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        if not is_admin_or_seller(request.user):
            raise PermissionDenied("Статистика доступна только администратору или продавцу")
        stats = Category.objects.aggregate(count=Count("id"))
        serializer = CountStatsSerializer(instance=stats)
        return Response(serializer.data)


class SupplierViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.query_params.get('name')
        phone = self.request.query_params.get('phone')
        if name:
            qs = qs.filter(name__icontains=name)
        if phone:
            qs = qs.filter(phone__icontains=phone)
        return qs

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        if not is_admin_or_seller(request.user):
            raise PermissionDenied("Статистика доступна только администратору или продавцу")
        stats = Supplier.objects.aggregate(count=Count("id"))
        serializer = CountStatsSerializer(instance=stats)
        return Response(serializer.data)


class PointOfSaleViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = PointOfSale.objects.all()
    serializer_class = PointOfSaleSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.query_params.get('name')
        address = self.request.query_params.get('address')
        if name:
            qs = qs.filter(name__icontains=name)
        if address:
            qs = qs.filter(address__icontains=address)
        return qs

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        if not is_admin_or_seller(request.user):
            raise PermissionDenied("Статистика доступна только администратору или продавцу")
        stats = PointOfSale.objects.aggregate(count=Count("id"))
        serializer = CountStatsSerializer(instance=stats)
        return Response(serializer.data)


class ProductViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Product.objects.all().annotate(
        has_pic=Q(picture__isnull=False) & ~Q(picture='')
    ).order_by('-has_pic', '-id')
    serializer_class = ProductSerializer
    pagination_class = CustomPagination 

    def get_queryset(self):
        qs = super().get_queryset()
        name = self.request.query_params.get('name')
        category_id = self.request.query_params.get('category')
        supplier_id = self.request.query_params.get('supplier')
        price_from = self.request.query_params.get('price_from')
        price_to = self.request.query_params.get('price_to')
        
        if name:
            qs = qs.filter(name__icontains=name)
        if category_id:
            qs = qs.filter(category_id=category_id)
        if supplier_id:
            qs = qs.filter(supplier_id=supplier_id)
        if price_from:
            qs = qs.filter(price__gte=price_from)
        if price_to:
            qs = qs.filter(price__lte=price_to)
        
        return qs

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        if not is_admin_or_seller(request.user):
            raise PermissionDenied("Статистика доступна только администратору или продавцу")
        
        stats = Product.objects.aggregate(
            count=Count("id"),
            avg_price=Avg("price"),
            max_price=Max("price"),
            min_price=Min("price")
        )
        
        stats = {k: (v if v is not None else 0) for k, v in stats.items()}
        
        serializer = ProductStatsSerializer(instance=stats)
        return Response(serializer.data)

class ProductImageViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class OrderViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = OrderSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        qs = Order.objects.all().order_by('-created_at')
        user = self.request.user
        
        if not user.is_authenticated:
            return qs.none()
        
        if not is_admin_or_seller(user):
            qs = qs.filter(user=user)
        
        qs = qs.annotate(
            calc_total_price=F('product__price') * F('quantity')
        )
        
        product_name = self.request.query_params.get('product')
        if product_name:
            qs = qs.filter(product__name__iexact=product_name)
        
        point_name = self.request.query_params.get('point')
        if point_name:
            qs = qs.filter(point__name__iexact=point_name)
        
        order_id = self.request.query_params.get('order_id')
        if order_id:
            qs = qs.filter(id__icontains=order_id)
        
        quantity = self.request.query_params.get('quantity')
        if quantity:
            qs = qs.filter(quantity__icontains=quantity)
        
        price_from = self.request.query_params.get('price_from')
        if price_from:
            qs = qs.filter(calc_total_price__gte=price_from)
        
        price_to = self.request.query_params.get('price_to')
        if price_to:
            qs = qs.filter(calc_total_price__lte=price_to)
        
        return qs

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["GET"], url_path="stats")
    def get_stats(self, request, *args, **kwargs):
        qs = self.get_queryset()
        stats = qs.aggregate(
            count=Count("id"),
            total_items=Sum("quantity"),
            total_sum=Sum(F('product__price') * F('quantity'))
        )
        serializer = OrderStatsSerializer(instance=stats)
        return Response(serializer.data)


class ProfileViewSet(GenericViewSet):
    queryset = User.objects.all()

    @action(detail=False, url_path="me", methods=['GET'])
    def get_me(self, request, *args, **kwargs):
        data = {'is_authenticated': self.request.user.is_authenticated}
        if self.request.user.is_authenticated:
            data.update({
                "username": self.request.user.username,
                "id": self.request.user.id,
                "is_superuser": self.request.user.is_superuser,
                "role": self.request.user.profile.role if hasattr(self.request.user, 'profile') else None,
            })
        return Response(data=data)

    @action(detail=False, url_path="logout", methods=['POST'])
    def logout(self, *args, **kwargs):
        django_logout(self.request)
        return Response()

    @action(detail=False, url_path="login", methods=['POST'])
    def login(self, *args, **kwargs):
        username = self.request.data['username']
        password = self.request.data['password']
        success = False
        status_code = 403
        user = authenticate(username=username, password=password)
        if user:
            success = True
            status_code = 200
            django_login(self.request, user)
        return Response({'success': success}, status=status_code)