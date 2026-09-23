from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from shop.models import Category, Supplier, PointOfSale, Product, Order


class CategoryViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        category = baker.make("shop.Category")
        r = self.client.get('/api/categories/')
        data = r.json()
        assert category.name == data[0]['name']
        assert category.id == data[0]['id']
        assert len(data) == 1


class SupplierViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        supplier = baker.make("shop.Supplier")
        r = self.client.get('/api/suppliers/')
        data = r.json()
        assert supplier.name == data[0]['name']
        assert supplier.id == data[0]['id']
        assert len(data) == 1


class PointOfSaleViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        point = baker.make("shop.PointOfSale")
        r = self.client.get('/api/points/')
        data = r.json()
        assert point.name == data[0]['name']
        assert point.id == data[0]['id']
        assert len(data) == 1


class ProductViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        category = baker.make("shop.Category")
        supplier = baker.make("shop.Supplier")
        product = baker.make("shop.Product", category=category, supplier=supplier)
        r = self.client.get('/api/products/')
        data = r.json()
        assert product.name == data[0]['name']
        assert product.id == data[0]['id']
        assert len(data) == 1


class OrderViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_get_list(self):
        category = baker.make("shop.Category")
        supplier = baker.make("shop.Supplier")
        product = baker.make("shop.Product", category=category, supplier=supplier)
        point = baker.make("shop.PointOfSale")
        order = baker.make("shop.Order", product=product, point=point)
        r = self.client.get('/api/orders/')
        data = r.json()
        assert order.id == data[0]['id']
        assert len(data) == 1