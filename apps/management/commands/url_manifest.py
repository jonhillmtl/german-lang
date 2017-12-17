from django.core.management.base import BaseCommand, CommandError
from utils import url_manifest

import pprint

class Command(BaseCommand):
    help = 'Populates the nouns'

    def handle(self, *args, **options):
        pprint.pprint(url_manifest())