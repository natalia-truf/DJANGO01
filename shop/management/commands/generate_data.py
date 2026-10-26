from django.core.management.base import BaseCommand
from faker import Faker
import random

from shop.models import Category, Supplier, PointOfSale, Product, Order
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])

        category_names = ['Футболки', 'Джинсы', 'Платья', 'Верхняя одежда', 'Аксессуары', 'Обувь', 'Спортивная одежда']
        for name in category_names:
            Category.objects.get_or_create(name=name)

        supplier_names = [
            'ООО "Текстиль-Пром"', 'ИП Иванов (Швейный цех)', 'ООО "Мода-Опт"', 
            'Фабрика "Красная нить"', 'ООО "Стиль Групп"', 'ТД "Одежда Плюс"',
            'ООО "Легпром"', 'ИП Смирнова (Трикотаж)', 'ООО "Деним-Трейд"',
            'Компания "Сезон"', 'ООО "Фэшн Логистик"', 'ООО "Швейпром"'
        ]
        for _ in range(1000):
            Supplier.objects.create(
                name=f"{random.choice(supplier_names)} {random.randint(1, 999)}",
                phone=fake.phone_number()
            )

        cities = ['Москва', 'Санкт-Петербург', 'Казань', 'Екатеринбург', 'Новосибирск', 'Нижний Новгород', 'Самара']
        streets = ['Ленина', 'Гагарина', 'Мира', 'Пушкина', 'Садовая', 'Советская', 'Центральная', 'Тверская']
        for _ in range(1000):
            PointOfSale.objects.create(
                name=f"Магазин на {random.choice(streets)}",
                address=f"г. {random.choice(cities)}, ул. {random.choice(streets)}, д. {random.randint(1, 150)}"
            )

        categories = list(Category.objects.all())
        suppliers = list(Supplier.objects.all())
        users = list(User.objects.all())
        
        if not users:
            users = [User.objects.create_user(username='testuser', password='password123')]

        product_names = [
            'Футболка', 'Джинсы', 'Платье', 'Куртка', 'Свитер', 'Пальто', 
            'Рубашка', 'Шорты', 'Юбка', 'Костюм', 'Пиджак', 'Кардиган',
            'Худи', 'Свитшот', 'Брюки', 'Блузка', 'Ветровка'
        ]
        colors = ['Белая', 'Черная', 'Синяя', 'Красная', 'Зеленая', 'Серая', 'Коричневая', 'Розовая', 'Бежевая', 'Голубая']
        materials = ['хлопка', 'шерсти', 'полиэстера', 'льна', 'кожи', 'денима', 'вискозы', 'кашемира']
        countries = ['Россия', 'Турция', 'Китай', 'Италия', 'Бангладеш', 'Вьетнам', 'Узбекистан', 'Индия']
        purposes = ['Повседневная носка', 'Деловой стиль', 'Спорт и фитнес', 'Вечерний выход', 'Отдых на природе', 'Домашний уют']
        genders = ['Мужская', 'Женская',]

        for _ in range(1000):
            prod_name = f"{random.choice(colors)} {random.choice(product_names).lower()}"
            
            gender = random.choice(genders)
            color = random.choice(colors).lower()
            material = random.choice(materials)
            country = random.choice(countries)
            purpose = random.choice(purposes)
            
            description = f"{gender} модель. Цвет: {color}. Материал: {material}. Назначение: {purpose.lower()}. Страна производства: {country}."
            
            Product.objects.create(
                name=prod_name,
                price=round(random.uniform(500, 15000), 2),
                category=random.choice(categories),
                supplier=random.choice(suppliers),
                description=description
            )

        products = list(Product.objects.all())
        points = list(PointOfSale.objects.all())

        for _ in range(1000):
            Order.objects.create(
                user=random.choice(users),
                product=random.choice(products),
                point=random.choice(points),
                quantity=random.randint(1, 5)
            )
            
        self.stdout.write(self.style.SUCCESS('Успешно сгенерировано!'))