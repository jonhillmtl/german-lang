from django.core.management.base import BaseCommand, CommandError
from api.models import Noun, UserStats
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Gets weak nouns'

    def handle(self, *args, **options):
        user = User.objects.get(pk=1)
        us = UserStats(user)
        print(us.weak_nouns())