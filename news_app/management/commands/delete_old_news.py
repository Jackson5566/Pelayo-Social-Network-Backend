# from datetime import timedelta
#
# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from news_app.models import NewsModel
#
#
# class Command(BaseCommand):
#     help = 'Eliminación de noticas pasadas de una semana'
#
#     def handle(self, *args, **options):
#         fecha_inicio = timezone.now() - timedelta(days=7)
#         try:
#             NewsModel.objects.delete(reated__gte=fecha_inicio)
#             self.stdout.write(self.style.SUCCESS('Todo correcto'))
#         except:
#             self.stdout.write(self.style.SUCCESS('Ha ocurrido un error'))
