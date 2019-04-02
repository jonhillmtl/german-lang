from django.core.management.base import BaseCommand
from utils import url_manifest
from typing import List, Dict

import pprint


class Command(BaseCommand):
    help = 'Populates the nouns'

    def handle(self, *args: List, **options: Dict) -> None:
        pprint.pprint(url_manifest())