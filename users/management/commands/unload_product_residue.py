from django.core.management.base import BaseCommand
from users.models import StockBalance, Product, Inventory
from django.db import transaction


class Command(BaseCommand):
    help = 'Удаляет данные остатков товаров (опционально с самими товарами)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Удалить все остатки товаров'
        )
        parser.add_argument(
            '--low-stock',
            action='store_true',
            help='Удалить только товары с низким запасом'
        )
        parser.add_argument(
            '--delete-products',
            action='store_true',
            help='Удалить также сами товары'
        )
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Подтвердить удаление без запроса'
        )

    def handle(self, *args, **options):
        delete_all = options['all']
        delete_low_stock = options['low_stock']
        delete_products = options['delete_products']
        confirm = options['confirm']

        if not delete_all and not delete_low_stock:
            self.stdout.write(self.style.ERROR('Укажите --all или --low-stock'))
            return

        queryset = StockBalance.objects.select_related('product').all()

        if delete_low_stock:
            queryset = [sb for sb in queryset if sb.is_low_stock()]
            message = f'Найдено {len(queryset)} товаров с низким запасом'
        else:
            message = f'Найдено {queryset.count()} остатков товаров'

        self.stdout.write(self.style.WARNING(message))

        if not confirm:
            self.stdout.write('Используйте --confirm для подтверждения удаления')
            return

        try:
            with transaction.atomic():
                if delete_products:
                    products_to_delete = [sb.product for sb in queryset]
                    self.stdout.write(self.style.WARNING(f'Удаление {len(products_to_delete)} товаров...'))
                    Product.objects.filter(id__in=[p.id for p in products_to_delete]).delete()
                else:
                    stock_ids = [sb.id for sb in queryset]
                    self.stdout.write(self.style.WARNING(f'Удаление {len(stock_ids)} остатков...'))
                    StockBalance.objects.filter(id__in=stock_ids).delete()

            self.stdout.write(self.style.SUCCESS('Данные успешно удалены'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при удалении: {str(e)}'))
