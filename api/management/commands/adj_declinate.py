from api.models import Adjective, Noun
from django.core.management.base import BaseCommand

import pprint


class Command(BaseCommand):
    help = 'Declinates nouns'

    def handle(self, *args, **options):
        for adjective in Adjective.objects.all():
            noun, choice_mode = Noun.random()

            print(adjective.adjective, noun.singular_form)
            pprint.pprint(adjective.declinate(noun))