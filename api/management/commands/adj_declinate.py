from api.models import Answer
from api.models import Adjective, Noun, UserStats, GrammarQueryStub
from api.serializers import NounSerializer

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count

import pprint


class Command(BaseCommand):
    help = 'Declinates nouns'

    def handle(self, *args, **options):
        for adjective in Adjective.objects.all():
            noun, choice_mode = Noun.random()

            print(adjective.adjective, noun.singular_form)
            pprint.pprint(adjective.declinate(noun))