from api.models import Answer
from api.models import Noun
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Gets nouns you have never done'

    def handle(self, *args, **options):
        user = User.objects.get(pk=1)

        answers = Answer.objects.filter(
            user=user,
            noun__isnull=False,
        ).values('noun__id')

        never_done = Noun.objects.exclude(id__in=answers)

        for n in never_done:
            print(n)
