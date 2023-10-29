from django.core.management.base import BaseCommand
from django.utils import timezone
from auth_app.models import User


class Command(BaseCommand):
    help = 'Eliminación de usuarios inactivos por más de 15 días'

    def handle(self, *args, **options):
        inactive_users = User.objects.filter(is_active=False)

        for user in inactive_users:
            if (timezone.now() - user.date_joined).days > 15:
                self.stdout.write(self.style.SUCCESS(f'Usuario eliminado: {user.username}'))
                user.delete()
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Usuario inactivo, pero con tiempo de cumplir su activación: {user.username}'))

        self.stdout.write(self.style.SUCCESS('Todo correcto'))
