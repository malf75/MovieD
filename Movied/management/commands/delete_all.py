from django.core.management.base import BaseCommand
from Movied.models import Filmes

class Command(BaseCommand):

    def delete_everything(self):
        Filmes.objects.all().delete()

    def handle(self, *args, **kwargs):
        self.delete_everything()