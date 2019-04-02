from api.models import Answer
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Count
from typing import List, Dict


class Command(BaseCommand):
    help = 'Gets weak nouns'

    def handle(self, *args: List, **options: Dict) -> None:
        user = User.objects.get(pk=1)

        answers = Answer.objects.filter(
            user=user,
            noun__isnull=False,
            correct=False
        ).values('noun', 'noun__singular_form').annotate(wrong_count=Count('noun')).order_by('-wrong_count')

        for answer in answers:
            print(answer)
