from api.models import Answer
from django.contrib.auth.models import User
from . import DocStringCommand
from django.db.models import Count
from typing import List, Dict


class Command(DocStringCommand):
    help = 'Gets nouns you have never done'

    def handle(self, *args: List, **options: Dict) -> None:
        """ The handler for this script. """

        user = User.objects.get(pk=1)

        answers = Answer.objects.filter(
            user=user,
            noun__isnull=False,
        ).values('noun', 'noun__singular_form').annotate(count=Count('noun')).order_by('count')

        for answer in answers:
            print(answer)
