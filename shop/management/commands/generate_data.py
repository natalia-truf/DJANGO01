from django.core.management.base import BaseCommand
from faker import Faker
import random
from tqdm import tqdm

from shop.models import Category, Supplier, PointOfSale, Product, Order
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker(['ru_RU'])

        if not Category.objects.exists():
            category_names = ['Одежда', 'Обувь', 'Аксессуары', 'Спорт', 'Дом']
            for name in tqdm(category_names, desc="Генерация категорий"):
                Category.objects.create(name=name)
        
        if not Supplier.objects.exists():
            for _ in tqdm(range(10), desc="Генерация поставщиков"):
                Supplier.objects.create(
                    name=fake.company(),
                    phone=fake.phone_number()
                )

        if not PointOfSale.objects.exists():
            for _ in tqdm(range(5), desc="Генерация точек продаж"):
                PointOfSale.objects.create(
                    name=f"Магазин {fake.street_name()}",
                    address=fake.address()
                )

        categories = list(Category.objects.all())
        suppliers = list(Supplier.objects.all())
        users = list(User.objects.all())
        points = list(PointOfSale.objects.all())

        if not categories or not suppliers or not points:
            self.stdout.write(self.style.ERROR('Не хватает данных для генерации!'))
            return

        product_names = ['Футболка', 'Джинсы', 'Платье', 'Куртка', 'Свитер', 'Рубашка', 'Шорты', 'Юбка', 'Костюм']
        colors = ['Белая', 'Черная', 'Синяя', 'Красная', 'Зеленая', 'Серая', 'Коричневая', 'Розовая', 'Бежевая']
        materials = ['хлопка', 'шерсти', 'полиэстера', 'льна', 'кожи']
        countries = ['Россия', 'Турция', 'Китай', 'Италия', 'Бангладеш', 'Вьетнам']
        purposes = ['Повседневная носка', 'Деловой стиль', 'Спорт и фитнес', 'Вечерний выход', 'Отдых']
        genders = ['Мужская', 'Женская', 'Унисекс']

        for _ in tqdm(range(1000), desc="Генерация товаров"):
            prod_name = f"{random.choice(colors)} {random.choice(product_names).lower()}"
            description = f"{random.choice(genders)} модель. Цвет: {random.choice(colors).lower()}. Материал: {random.choice(materials)}. Назначение: {random.choice(purposes).lower()}. Страна: {random.choice(countries)}."
            
            Product.objects.create(
                name=prod_name,
                price=round(random.uniform(500, 15000), 2),
                category=random.choice(categories),
                supplier=random.choice(suppliers),
                description=description
            )

        products = list(Product.objects.all())

        for _ in tqdm(range(1000), desc="Генерация заказов"):
            Order.objects.create(
                user=random.choice(users),
                product=random.choice(products),
                point=random.choice(points),
                quantity=random.randint(1, 5)
            )
            
        self.stdout.write(self.style.SUCCESS('Успешно сгенерировано всё необходимое!'))