from django.core.management.base import BaseCommand
from users.models import StockBalance
import csv
import json
from datetime import datetime


class Command(BaseCommand):
    help = 'Экспортирует данные остатков товаров в CSV или JSON файл'

    def add_arguments(self, parser):
        parser.add_argument(
            'output_file',
            type=str,
            help='Путь к выходному файлу'
        )
        parser.add_argument(
            '--format',
            type=str,
            choices=['csv', 'json'],
            default='csv',
            help='Формат экспорта (csv или json)'
        )
        parser.add_argument(
            '--low-stock-only',
            action='store_true',
            help='Экспортировать только товары с низким запасом'
        )

    def handle(self, *args, **options):
        output_file = options['output_file']
        file_format = options['format']
        low_stock_only = options['low_stock_only']

        queryset = StockBalance.objects.select_related('product').all()

        if low_stock_only:
            queryset = [sb for sb in queryset if sb.is_low_stock()]
            self.stdout.write(self.style.WARNING(f'Экспорт {len(queryset)} товаров с низким запасом'))
        else:
            self.stdout.write(self.style.WARNING(f'Экспорт {queryset.count()} товаров'))

        try:
            if file_format == 'csv':
                self.export_to_csv(queryset, output_file)
            elif file_format == 'json':
                self.export_to_json(queryset, output_file)

            self.stdout.write(self.style.SUCCESS(f'Данные успешно экспортированы в {output_file}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при экспорте: {str(e)}'))

    def export_to_csv(self, queryset, output_file):
        with open(output_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow([
                'ID товара',
                'Название товара',
                'Категория',
                'Текущее количество',
                'Зарезервировано',
                'Доступно',
                'Минимальный запас',
                'Низкий запас',
                'Дата последнего пополнения',
                'Дата последнего обновления'
            ])

            for stock_balance in queryset:
                writer.writerow([
                    stock_balance.product.id,
                    stock_balance.product.name,
                    stock_balance.product.category.name,
                    stock_balance.quantity,
                    stock_balance.reserved_quantity,
                    stock_balance.available_quantity,
                    stock_balance.minimum_stock,
                    'Да' if stock_balance.is_low_stock() else 'Нет',
                    stock_balance.last_restocked.strftime('%Y-%m-%d %H:%M:%S') if stock_balance.last_restocked else '',
                    stock_balance.last_updated.strftime('%Y-%m-%d %H:%M:%S')
                ])

    def export_to_json(self, queryset, output_file):
        data = []
        for stock_balance in queryset:
            data.append({
                'product_id': stock_balance.product.id,
                'product_name': stock_balance.product.name,
                'category': stock_balance.product.category.name,
                'quantity': stock_balance.quantity,
                'reserved_quantity': stock_balance.reserved_quantity,
                'available_quantity': stock_balance.available_quantity,
                'minimum_stock': stock_balance.minimum_stock,
                'is_low_stock': stock_balance.is_low_stock(),
                'last_restocked': stock_balance.last_restocked.strftime('%Y-%m-%d %H:%M:%S') if stock_balance.last_restocked else None,
                'last_updated': stock_balance.last_updated.strftime('%Y-%m-%d %H:%M:%S')
            })

        with open(output_file, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=2)
