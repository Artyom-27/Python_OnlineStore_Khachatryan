from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass



class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название категории")

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, verbose_name="Пользователь")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Отчество")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(max_length=100, verbose_name="Email")

    # Разделенный адрес
    country = models.CharField(max_length=50, verbose_name="Страна")
    city = models.CharField(max_length=50, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house_number = models.CharField(max_length=10, verbose_name="Номер дома")
    apartment_number = models.CharField(max_length=10, blank=True, null=True, verbose_name="Номер квартиры")
    postal_code = models.CharField(max_length=15, verbose_name="Почтовый индекс")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='products/', verbose_name="Изображение товара")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")

    def __str__(self):
        return self.name


class Inventory(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity_in_stock = models.IntegerField(verbose_name="Количество на складе")
    warehouse_section = models.CharField(max_length=50, blank=True, null=True, verbose_name="Секция склада")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")

    def __str__(self):
        return f"Запас для {self.product.name}: {self.quantity_in_stock} шт."


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name="Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Добавлено в корзину")

    def __str__(self):
        return f"Корзина {self.user.username if self.user else 'Гость'} - {self.product.name} ({self.quantity} шт.)"


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    def add_item(self, product, quantity=1):
        cart_item, created = CartItem.objects.get_or_create(
            user=self.user,
            product=product,
            defaults={'quantity': quantity}
        )
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        return cart_item

    def remove_item(self, product):
        CartItem.objects.filter(user=self.user, product=product).delete()

    def clear(self):
        CartItem.objects.filter(user=self.user).delete()

    @property
    def total_price(self):
        total = 0
        for item in CartItem.objects.filter(user=self.user):
            total += item.product.price * item.quantity
        return total

    @property
    def total_items(self):
        return CartItem.objects.filter(user=self.user).count()


class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('paid', 'Оплачен'),
        ('shipped', 'Доставляется'),
        ('delivered', 'Доставлен'),
        ('canceled', 'Отменен'),
    ]

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True, verbose_name="Пользователь")
    order_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата заказа")
    order_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='new', verbose_name="Статус заказа")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая сумма")

    def __str__(self):
        return f"Заказ №{self.id} от {self.order_date.strftime('%d.%m.%Y')}"


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена при покупке")

    def __str__(self):
        return f"Позиция заказа №{self.order.id}: {self.product.name}"


class StockBalance(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.IntegerField(default=0, verbose_name="Текущее количество")
    reserved_quantity = models.IntegerField(default=0, verbose_name="Зарезервировано")
    minimum_stock = models.IntegerField(default=10, verbose_name="Минимальный запас")
    last_restocked = models.DateTimeField(blank=True, null=True, verbose_name="Дата последнего пополнения")
    last_updated = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")

    def __str__(self):
        return f"Баланс {self.product.name}: {self.quantity} шт. (зарезервировано: {self.reserved_quantity})"

    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity

    def is_low_stock(self):
        return self.available_quantity < self.minimum_stock
