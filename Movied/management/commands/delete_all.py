from django.core.management.base import BaseCommand
from django.db import connection
from Movied.models import Notifications

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        with connection.schema_editor() as schema_editor:

            Notifications.user.objects.filter(notifications_id__in=Notifications.objects.values_list('id', flat=True)).delete()
            
            schema_editor.execute("DROP TABLE IF EXISTS Movied_notifications")