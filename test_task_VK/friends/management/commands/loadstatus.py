import json
import os

from django.core.management.base import BaseCommand

from friends.models import Status
from test_task_VK.settings import BASE_DIR

DATA_DIR = os.path.join(BASE_DIR, 'data')


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(
            os.path.join(DATA_DIR, 'status.json'),
            encoding='utf-8'
        ) as data:
            statuses = json.loads(data.read())
            for status in statuses:
                Status.objects.get_or_create(**status)
