from django.core.management.base import BaseCommand
from newspaper_app.models import NewspaperModel


class Command(BaseCommand):
    help = 'Eliminacion de el periodico'

    def handle(self, *args, **options):
        try:
            NewspaperModel.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Todo correcto'))
        except:
            self.stdout.write(self.style.SUCCESS('Ha ocurrido un error'))
