from api.models import Answer
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Count


class Command(BaseCommand):
    help = 'Gets nouns you have never done'

    def handle(self, *args, **options):
        user = User.objects.get(pk=1)

        answers = Answer.objects.filter(
            user=user,
            noun__isnull=False,
        ).values('noun', 'noun__singular_form').annotate(count=Count('noun')).order_by('count')

        for answer in answers:
            print(answer)