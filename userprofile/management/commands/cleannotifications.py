from django.core.management.base import BaseCommand
from notify.models import Notification

class Command(BaseCommand):
    help = 'Cleans notifications marked as deleted'

    def handle(self, *args, **options):
        # pylint: disable=E1101
        count = 0
        for notif in Notification.objects.all():
            if notif.deleted:
                print(notif)
                notif.delete()
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Cleaned {count} notifications'))
