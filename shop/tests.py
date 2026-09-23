from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker

from shop.models import Category, Supplier, PointOfSale, Product, Order


#CATEGORY

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

    def test_create(self):
        r = self.client.post('/api/categories/', {
            "name": "Футболки"
        })
        new_id = r.json()['id']
        categories = Category.objects.all()
        assert len(categories) == 1
        new_category = Category.objects.filter(id=new_id).first()
        assert new_category.name == 'Футболки'

    def test_delete(self):
        categories = baker.make("shop.Category", _quantity=10)
        r = self.client.get('/api/categories/')
        data = r.json()
        assert len(data) == 10

        category_id_to_delete = categories[3].id
        self.client.delete(f'/api/categories/{category_id_to_delete}/')

        r = self.client.get('/api/categories/')
        data = r.json()
        assert len(data) == 9
        assert category_id_to_delete not in [i['id'] for i in data]

    def test_update(self):
        categories = baker.make("shop.Category", _quantity=10)
        category = categories[2]

        r = self.client.get(f'/api/categories/{category.id}/')
        data = r.json()
        assert data['name'] == category.name

        r = self.client.put(f'/api/categories/{category.id}/', {
            "name": "Новая категория"
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/categories/{category.id}/')
        data = r.json()
        assert data['name'] == "Новая категория"

        category.refresh_from_db()
        assert data['name'] == category.name


#SUPPLIER

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

    def test_create(self):
        r = self.client.post('/api/suppliers/', {
            "name": "ООО Мода",
            "phone": "8-800-123-45-67"
        })
        new_id = r.json()['id']
        suppliers = Supplier.objects.all()
        assert len(suppliers) == 1
        new_supplier = Supplier.objects.filter(id=new_id).first()
        assert new_supplier.name == 'ООО Мода'
        assert new_supplier.phone == '8-800-123-45-67'

    def test_delete(self):
        suppliers = baker.make("shop.Supplier", _quantity=10)
        r = self.client.get('/api/suppliers/')
        data = r.json()
        assert len(data) == 10

        supplier_id_to_delete = suppliers[3].id
        self.client.delete(f'/api/suppliers/{supplier_id_to_delete}/')

        r = self.client.get('/api/suppliers/')
        data = r.json()
        assert len(data) == 9
        assert supplier_id_to_delete not in [i['id'] for i in data]

    def test_update(self):
        suppliers = baker.make("shop.Supplier", _quantity=10)
        supplier = suppliers[2]

        r = self.client.get(f'/api/suppliers/{supplier.id}/')
        data = r.json()
        assert data['name'] == supplier.name

        r = self.client.put(f'/api/suppliers/{supplier.id}/', {
            "name": "Новый поставщик",
            "phone": "8-800-000-00-00"
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/suppliers/{supplier.id}/')
        data = r.json()
        assert data['name'] == "Новый поставщик"

        supplier.refresh_from_db()
        assert data['name'] == supplier.name


#POINT OF SALE

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

    def test_create(self):
        r = self.client.post('/api/points/', {
            "name": "Магазин на Ленина",
            "address": "ул. Ленина, 10"
        })
        new_id = r.json()['id']
        points = PointOfSale.objects.all()
        assert len(points) == 1
        new_point = PointOfSale.objects.filter(id=new_id).first()
        assert new_point.name == 'Магазин на Ленина'
        assert new_point.address == 'ул. Ленина, 10'

    def test_delete(self):
        points = baker.make("shop.PointOfSale", _quantity=10)
        r = self.client.get('/api/points/')
        data = r.json()
        assert len(data) == 10

        point_id_to_delete = points[3].id
        self.client.delete(f'/api/points/{point_id_to_delete}/')

        r = self.client.get('/api/points/')
        data = r.json()
        assert len(data) == 9
        assert point_id_to_delete not in [i['id'] for i in data]

    def test_update(self):
        points = baker.make("shop.PointOfSale", _quantity=10)
        point = points[2]

        r = self.client.get(f'/api/points/{point.id}/')
        data = r.json()
        assert data['name'] == point.name

        r = self.client.put(f'/api/points/{point.id}/', {
            "name": "Новая точка",
            "address": "ул. Пушкина, 5"
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/points/{point.id}/')
        data = r.json()
        assert data['name'] == "Новая точка"

        point.refresh_from_db()
        assert data['name'] == point.name


# PRODUCT

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

    def test_create(self):
        category = baker.make("shop.Category")
        supplier = baker.make("shop.Supplier")
        r = self.client.post('/api/products/', {
            "name": "Футболка",
            "price": "1200.00",
            "category_id": category.id,
            "supplier_id": supplier.id,
            "description": "Тестовая футболка"
        })
        new_id = r.json()['id']
        products = Product.objects.all()
        assert len(products) == 1
        new_product = Product.objects.filter(id=new_id).first()
        assert new_product.name == 'Футболка'
        assert new_product.category == category
        assert new_product.supplier == supplier

    def test_delete(self):
        category = baker.make("shop.Category")
        supplier = baker.make("shop.Supplier")
        products = baker.make("shop.Product", category=category, supplier=supplier, _quantity=10)

        r = self.client.get('/api/products/')
        data = r.json()
        assert len(data) == 10

        product_id_to_delete = products[3].id
        self.client.delete(f'/api/products/{product_id_to_delete}/')

        r = self.client.get('/api/products/')
        data = r.json()
        assert len(data) == 9
        assert product_id_to_delete not in [i['id'] for i in data]

    def test_update(self):
        category = baker.make("shop.Category")
        supplier = baker.make("shop.Supplier")
        products = baker.make("shop.Product", category=category, supplier=supplier, _quantity=10)
        product = products[2]

        r = self.client.get(f'/api/products/{product.id}/')
        data = r.json()
        assert data['name'] == product.name

        r = self.client.put(f'/api/products/{product.id}/', {
            "name": "Новый товар",
            "price": "999.00",
            "category_id": category.id,
            "supplier_id": supplier.id,
            "description": "Обновлённое описание"
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/products/{product.id}/')
        data = r.json()
        assert data['name'] == "Новый товар"

        product.refresh_from_db()
        assert data['name'] == product.name


#ORDER

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

    def test_create(self):
        category = baker.make("shop.Category")
        supplier = baker.make("shop.Supplier")
        product = baker.make("shop.Product", category=category, supplier=supplier)
        point = baker.make("shop.PointOfSale")
        r = self.client.post('/api/orders/', {
            "product_id": product.id,
            "point_id": point.id,
            "quantity": 3
        })
        new_id = r.json()['id']
        orders = Order.objects.all()
        assert len(orders) == 1
        new_order = Order.objects.filter(id=new_id).first()
        assert new_order.product == product
        assert new_order.point == point
        assert new_order.quantity == 3

    def test_delete(self):
        category = baker.make("shop.Category")
        supplier = baker.make("shop.Supplier")
        product = baker.make("shop.Product", category=category, supplier=supplier)
        point = baker.make("shop.PointOfSale")
        orders = baker.make("shop.Order", product=product, point=point, _quantity=10)

        r = self.client.get('/api/orders/')
        data = r.json()
        assert len(data) == 10

        order_id_to_delete = orders[3].id
        self.client.delete(f'/api/orders/{order_id_to_delete}/')

        r = self.client.get('/api/orders/')
        data = r.json()
        assert len(data) == 9
        assert order_id_to_delete not in [i['id'] for i in data]

    def test_update(self):
        category = baker.make("shop.Category")
        supplier = baker.make("shop.Supplier")
        product = baker.make("shop.Product", category=category, supplier=supplier)
        point = baker.make("shop.PointOfSale")
        orders = baker.make("shop.Order", product=product, point=point, _quantity=10)
        order = orders[2]

        r = self.client.get(f'/api/orders/{order.id}/')
        data = r.json()
        assert data['quantity'] == order.quantity

        r = self.client.put(f'/api/orders/{order.id}/', {
            "product_id": product.id,
            "point_id": point.id,
            "quantity": 99
        })
        assert r.status_code == 200

        r = self.client.get(f'/api/orders/{order.id}/')
        data = r.json()
        assert data['quantity'] == 99

        order.refresh_from_db()
        assert data['quantity'] == order.quantity