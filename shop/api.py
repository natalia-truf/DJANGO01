from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from shop.models import Product, Category, Supplier, PointOfSale, Order, ProductImage, Profile
from shop.serializers import (
    ProductSerializer, CategorySerializer, SupplierSerializer,
    PointOfSaleSerializer, OrderSerializer, ProductImageSerializer, ProfileSerializer
)

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 10000

class CategoryViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None  # <-- Отключаем пагинацию для категорий


class SupplierViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    pagination_class = CustomPagination


class PointOfSaleViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                         mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = PointOfSale.objects.all()
    serializer_class = PointOfSaleSerializer
    pagination_class = CustomPagination

from django.db.models import Q

class ProductViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    
    queryset = Product.objects.all().annotate(
        has_pic=Q(picture__isnull=False) & ~Q(picture='')
    ).order_by('-has_pic', '-id')
    
    serializer_class = ProductSerializer
    pagination_class = CustomPagination 

class ProductImageViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class OrderViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if not user.is_authenticated:
            return qs.none()

        if user.is_superuser:
            return qs

        if hasattr(user, 'profile') and user.profile.role == 'admin':
            return qs

        return qs.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProfileViewSet(GenericViewSet):
    queryset = User.objects.all()

    @action(detail=False, url_path="me", methods=['GET'])
    def get_me(self, request, *args, **kwargs):
        data = {
            'is_authenticated': self.request.user.is_authenticated
        }

        if self.request.user.is_authenticated:
            data.update({
                "username": self.request.user.username,
                "id": self.request.user.id,
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

        return Response({
            'success': success
        }, status=status_code)