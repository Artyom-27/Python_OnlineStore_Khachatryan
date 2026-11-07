from django.core.management.base import BaseCommand
from django.db import transaction
from users.models import Product, Category, Inventory, StockBalance
import csv
import json


class Command(BaseCommand):
    help = 'Загружает товары из CSV или JSON файла'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            type=str,
            help='Путь к файлу с данными (CSV или JSON)'
        )
        parser.add_argument(
            '--format',
            type=str,
            choices=['csv', 'json'],
            default='csv',
            help='Формат файла (csv или json)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить существующие товары перед загрузкой'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        file_format = options['format']
        clear_existing = options['clear']

        if clear_existing:
            self.stdout.write(self.style.WARNING('Очистка существующих товаров...'))
            Product.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Существующие товары удалены'))

        try:
            if file_format == 'csv':
                self.load_from_csv(file_path)
            elif file_format == 'json':
                self.load_from_json(file_path)

            self.stdout.write(self.style.SUCCESS('Успешно загружены товары'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке: {str(e)}'))

    def load_from_csv(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            with transaction.atomic():
                for row in reader:
                    category, _ = Category.objects.get_or_create(
                        name=row.get('category', 'Без категории')
                    )

                    product = Product.objects.create(
                        name=row['name'],
                        description=row.get('description', ''),
                        price=row['price'],
                        category=category
                    )

                    # Создаем запись в Inventory
                    Inventory.objects.create(
                        product=product,
                        quantity_in_stock=int(row.get('quantity', 0)),
                        warehouse_section=row.get('warehouse_section', '')
                    )

                    # Создаем запись в StockBalance
                    StockBalance.objects.create(
                        product=product,
                        quantity=int(row.get('quantity', 0)),
                        minimum_stock=int(row.get('minimum_stock', 10))
                    )

                    self.stdout.write(f'Загружен товар: {product.name}')

    def load_from_json(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            with transaction.atomic():
                for item in data:
                    category, _ = Category.objects.get_or_create(
                        name=item.get('category', 'Без категории')
                    )

                    product = Product.objects.create(
                        name=item['name'],
                        description=item.get('description', ''),
                        price=item['price'],
                        category=category
                    )

                    # Создаем запись в Inventory
                    Inventory.objects.create(
                        product=product,
                        quantity_in_stock=int(item.get('quantity', 0)),
                        warehouse_section=item.get('warehouse_section', '')
                    )

                    # Создаем запись в StockBalance
                    StockBalance.objects.create(
                        product=product,
                        quantity=int(item.get('quantity', 0)),
                        minimum_stock=int(item.get('minimum_stock', 10))
                    )

                    self.stdout.write(f'Загружен товар: {product.name}')
