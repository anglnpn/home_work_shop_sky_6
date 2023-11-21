from django.core.management import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):

    def handle(self, *args, **options):
        category_list = [
            {'name': 'Сладости', 'description': 'Сладости'},
            {'name': 'Крупы', 'description': 'Крупы'}
        ]

        for category_item in category_list:
            Category.objects.create(**category_item)

        product_list = [
            {'name': 'Шоколад', 'description': 'Молочный', 'category': 'Сладости',
             'price': '200', 'create_date': '2023-11-20T13:48:36Z', 'edit_date': '2023-11-20T13:48:36Z'},
            {'name': 'Рис', 'description': 'черный', 'category': 'Крупы',
             'price': '100', 'create_date': '2023-11-20T13:48:36Z', 'edit_date': '2023-11-20T13:48:36Z'}
        ]

        for product_item in product_list:
            Product.objects.create(**product_item)
