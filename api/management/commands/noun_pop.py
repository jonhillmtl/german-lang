from django.core.management.base import BaseCommand, CommandError
from api.models import Noun

class Command(BaseCommand):
    help = 'Populates the nouns'

    def handle(self, *args, **options):
        with open("./data/nouns.csv", "r") as f:
            for line in f.readlines()[1:]:
                values = line.split(',')

                # TODO JHILL: check for doubles
                # TODO JHILL: sanitize
                # TODO JHILL: add translations
                # TODO JHILL: add language

                noun = Noun()
                noun.singular_form = values[0]
                noun.plural_form = values[1]
                noun.gender = values[2]
                noun.save()