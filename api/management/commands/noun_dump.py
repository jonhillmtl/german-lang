from django.core.management.base import BaseCommand, CommandError
from api.models import Noun, Translation
from text_header import text_header
import pprint

class Command(BaseCommand):
    help = 'Dumps a noun or all nouns'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--noun_id',
            dest='noun_id',
            default=False,
            help='',
        )

    def handle(self, *args, **options):
        if options['noun_id'] is not None:
            nouns = [Noun.objects.get(pk=options['noun_id'])]
        else:
            nouns = Noun.objects.all()

        for noun in nouns:
            print(noun.id, noun)
            pprint.pprint(noun.articled)
