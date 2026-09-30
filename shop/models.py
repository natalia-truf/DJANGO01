from django.db import models

class Category(models.Model):
    name = models.TextField("Название")
    picture = models.ImageField("Изображение", null=True, upload_to="categories")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Supplier(models.Model):
    name = models.TextField("Название")
    phone = models.TextField("Телефон")

    class Meta:
        verbose_name = "Поставщик"
        verbose_name_plural = "Поставщики"

    def __str__(self):
        return self.name


class PointOfSale(models.Model):
    name = models.TextField("Название")
    address = models.TextField("Адрес")

    class Meta:
        verbose_name = "Точка продажи"
        verbose_name_plural = "Точки продажи"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.TextField("Название")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name="Поставщик")
    description = models.TextField("Описание", blank=True)
    picture = models.ImageField("Изображение", null=True, upload_to="products")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    point = models.ForeignKey(PointOfSale, on_delete=models.CASCADE, verbose_name="Точка продажи")
    quantity = models.IntegerField(default=1, verbose_name="Количество")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.id}"