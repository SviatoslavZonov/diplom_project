# командf для ожидания Redis
import time
from django.core.management.base import BaseCommand
from django_redis import get_redis_connection
from redis.exceptions import ConnectionError

class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write('Waiting for Redis...')
        while True:
            try:
                conn = get_redis_connection("default")
                conn.ping()
                self.stdout.write(self.style.SUCCESS('Redis available!'))
                break
            except ConnectionError:
                self.stdout.write('Redis unavailable, waiting 1 second...')
                time.sleep(1)