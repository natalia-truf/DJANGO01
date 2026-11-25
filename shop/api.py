from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission, IsAuthenticated

from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Count, Sum, Avg, Max, Min, F
from django.http import HttpResponse
from django.core.cache import cache

from openpyxl import Workbook
from openpyxl.styles import Font

import pyotp
import qrcode
import base64
from io import BytesIO

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

    @action(detail=False, methods=["GET"], url_path="unique-prices")
    def get_unique_prices(self, request, *args, **kwargs):
        prices = Product.objects.values_list('price', flat=True).distinct().order_by('price')
        return Response([str(p) for p in prices])

class ProductImageViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                          mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class OrderViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    serializer_class = OrderSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), UserProfileViewSet.OTPRequired()]
        return [IsAuthenticated()]

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

    @action(detail=False, methods=["GET"], url_path="export-excel")
    def export_excel(self, request, *args, **kwargs):
        qs = self.get_queryset()

        wb = Workbook()
        ws = wb.active
        ws.title = "Заказы"

        headers = ["ID заказа", "Товар", "Точка продажи", "Количество", "Сумма (руб.)", "Дата"]
        ws.append(headers)

        for cell in ws[1]:
            cell.font = Font(bold=True)

        for order in qs:
            ws.append([
                order.id,
                order.product.name if order.product else "Удален",
                order.point.name if order.point else "Удалена",
                order.quantity,
                float(order.total_price),
                order.created_at.strftime("%d.%m.%Y %H:%M")
            ])

        ws.column_dimensions['A'].width = 10
        ws.column_dimensions['B'].width = 30
        ws.column_dimensions['C'].width = 25
        ws.column_dimensions['D'].width = 12
        ws.column_dimensions['E'].width = 15
        ws.column_dimensions['F'].width = 20

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=orders_export.xlsx'
        wb.save(response)
        return response

class UserProfileViewSet(GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    class OTPSerializer(serializers.Serializer):
        key = serializers.CharField()

    class OTPRequired(BasePermission):
        def has_permission(self, request, view):
            return bool(request.user and cache.get('otp_good', False))

    @action(detail=False, url_path="check-login", methods=['GET'], permission_classes=[])
    def get_check_login(self, request, *args, **kwargs):
        return Response({
            'is_authenticated': self.request.user.is_authenticated
        })

    @action(detail=False, url_path="use-login", methods=['POST'], permission_classes=[])
    def use_login(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            django_login(request, user)
        return Response({
            'is_authenticated': bool(user)
        })

    @action(detail=False, url_path='otp-login', methods=['POST'], serializer_class=OTPSerializer)
    def otp_login(self, request, *args, **kwargs):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        if not profile.otp_key:
            return Response({'success': False, 'error': 'OTP не настроен'})

        totp = pyotp.TOTP(profile.otp_key)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        success = False
        if totp.now() == serializer.validated_data['key']:
            cache.set('otp_good', True, 600)
            success = True

        return Response({
            'success': success
        })

    @action(detail=False, url_path='otp-status')
    def get_otp_status(self, request, *args, **kwargs):
        otp_good = cache.get('otp_good', False)
        return Response({
            'otp_good': otp_good
        })

    @action(detail=False, url_path='otp-required', permission_classes=[OTPRequired])
    def page_with_otp_required(self, request, *args, **kwargs):
        return Response({
            'success': True
        })

    @action(detail=False, url_path="me", methods=['GET'], permission_classes=[])
    def get_me(self, request, *args, **kwargs):
        data = {'is_authenticated': self.request.user.is_authenticated}
        if self.request.user.is_authenticated:
            profile, _ = Profile.objects.get_or_create(user=request.user)
            data.update({
                "username": self.request.user.username,
                "id": self.request.user.id,
                "is_superuser": self.request.user.is_superuser,
                "role": profile.role,
                "otp_enabled": bool(profile.otp_key),
            })
        return Response(data=data)

    @action(detail=False, url_path="logout", methods=['POST'], permission_classes=[])
    def logout(self, request, *args, **kwargs):
        django_logout(request)
        return Response()

    @action(detail=False, url_path="login", methods=['POST'], permission_classes=[])
    def login(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        success = False
        status_code = 403
        user = authenticate(username=username, password=password)
        if user:
            success = True
            status_code = 200
            django_login(request, user)
        return Response({'success': success}, status=status_code)

    @action(detail=False, url_path="otp-setup", methods=['GET'])
    def otp_setup(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'Не авторизован'}, status=401)

        profile, _ = Profile.objects.get_or_create(user=request.user)

        otp_key = pyotp.random_base32()
        profile.otp_key = otp_key
        profile.save()

        otp_uri = pyotp.totp.TOTP(otp_key).provisioning_uri(
            name=request.user.username,
            issuer_name="Магазин"
        )

        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(otp_uri)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

        return Response({
            'otp_key': otp_key,
            'qr_code': f'data:image/png;base64,{qr_base64}',
            'manual_key': otp_key
        })

    @action(detail=False, url_path="register", methods=['POST'], permission_classes=[])
    def register(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        role = request.data.get('role', 'buyer')
    
        if not username or not password:
            return Response({'error': 'Логин и пароль обязательны'}, status=400)
    
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Пользователь с таким логином уже существует'}, status=400)
    
        user = User.objects.create_user(username=username, password=password)
        Profile.objects.create(user=user, role=role)
    
        django_login(request, user)
                
        return Response({'success': True, 'message': 'Регистрация успешна'}, status=201)

    @action(detail=False, url_path="otp-disable", methods=['POST'])
    def otp_disable(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'Не авторизован'}, status=401)

        profile, _ = Profile.objects.get_or_create(user=request.user)
        profile.otp_key = ''
        profile.save()
        cache.delete('otp_good')

        return Response({'success': True})