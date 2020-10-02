from django.core.management.base import BaseCommand
import user_app.models as md
import datetime
import subprocess


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        rooms = md.ValidRoom.objects.all()
        for room in rooms:
            delta = room.date - datetime.datetime.now(datetime.timezone.utc)
            if delta < datetime.timedelta(seconds=12):
                subprocess.run(['turnadmin', '-d', '-u' + room.validation_username.strip(), '-r', 'default'])
                md.ValidRoom.objects.filter(id=room.id).delete()
