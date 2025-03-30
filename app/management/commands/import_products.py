import yaml
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from app.models import Product, Supplier

class Command(BaseCommand):  # Обязательно назвать класс Command
    help = 'Импорт товаров из YAML-файлов'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            help='Custom path to YAML files directory',
            default=os.path.join(settings.BASE_DIR, 'data')
        )

    def handle(self, *args, **options):
        path = options['path']
        self.stdout.write(self.style.SUCCESS(f'Starting import from: {path}'))
        
        for filename in os.listdir(path):
            if filename.endswith(('.yaml', '.yml')):
                self.import_file(os.path.join(path, filename))

    def import_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:  # Добавлено encoding
                data = yaml.safe_load(f)
                for item in data.get('products', []):
                    self.process_product(item)
            self.stdout.write(self.style.SUCCESS(f'Processed: {os.path.basename(file_path)}'))
        except UnicodeDecodeError:
            self.stdout.write(self.style.ERROR(
                f"Ошибка кодировки в файле {file_path}. Сохраните файл в UTF-8!"
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error in {file_path}: {str(e)}'))

    def process_product(self, data):
        try:
            supplier, _ = Supplier.objects.get_or_create(
                name=data['supplier'],
                defaults={'is_active': True}
            )
            
            Product.objects.update_or_create(
                name=data['name'],
                supplier=supplier,
                defaults={
                    'description': data.get('description', ''),
                    'price': data['price'],
                    'quantity': data.get('quantity', 0),
                    'characteristics': data.get('characteristics', {})
                }
            )
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f'Missing field {e} in product data'))