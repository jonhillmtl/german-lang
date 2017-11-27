from django.core.management.base import BaseCommand, CommandError
from api.models import Noun, UserStats, GrammarQueryStub
from api.serializers import NounSerializer
import pprint

from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Gets weak nouns'

    def handle(self, *args, **options):
        user = User.objects.get(pk=1)
        query_stub = GrammarQueryStub(user=user)
        noun, choice_mode = Noun.random(query_stub)
        
        pprint.pprint(NounSerializer(noun).data)
