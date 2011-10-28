from django.core.management.base import BaseCommand
from django.core.cache import cache
from redis.exceptions import ResponseError

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            cache.clear()
        except ResponseError:
            cache.clear()
        self.stdout.write('Cleared cache\n')
