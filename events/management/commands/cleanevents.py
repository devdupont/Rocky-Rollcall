from django.core.management.base import BaseCommand
from events.models import Event

class Command(BaseCommand):
    help = 'Cleans expired events'

    def handle(self, *args, **options):
        # pylint: disable=E1101
        count = 0
        for event in Event.objects.all():
            if event.is_expired:
                print(event)
                event.delete()
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Cleaned {count} events'))
