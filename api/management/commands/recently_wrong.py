from api.models import Answer
from api.models import Noun, UserStats, GrammarQueryStub
from api.serializers import NounSerializer

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db.models import Count

import pprint


class Command(BaseCommand):
    help = 'Gets nouns you have never done'

    def handle(self, *args, **options):
        user = User.objects.get(pk=1)

        answers = Answer.objects.filter(
            user=user,
            noun__isnull=False,
            correct=False
        ).values('noun', 'noun__singular_form', 'created_at').order_by('-created_at')

        for answer in answers:
            print(answer)
