from django.core.management.base import BaseCommand

from diogenis.local_settings import REDIS as r

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for key in r.keys('*sessions.cache*'):
            r.delete(key)
        self.stdout.write('Cleared cached sessions\n') 
