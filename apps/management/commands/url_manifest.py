from django.core.management.base import BaseCommand
from utils import url_manifest
from typing import List, Dict

import pprint


class Command(BaseCommand):
    """ Populates the nouns. """

    help = 'Populates the nouns'

    def handle(self, *args: List, **options: Dict) -> None:
        """ The handler for this script. """

        pprint.pprint(url_manifest())
