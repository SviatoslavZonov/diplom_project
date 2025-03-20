import yaml
from django.core.management.base import BaseCommand
from app.models import Product, Supplier

class Command(BaseCommand):
    help = 'Import products from YAML file'

    def handle(self, *args, **kwargs):
        with open('data/shop1.yaml', 'r') as file:
            data = yaml.safe_load(file)
            for item in data['products']:
                supplier, _ = Supplier.objects.get_or_create(name=item['supplier'])
                Product.objects.create(
                    name=item['name'],
                    supplier=supplier,
                    price=item['price'],
                    description=item['description']
                )
            self.stdout.write(self.style.SUCCESS('Products imported successfully'))
            