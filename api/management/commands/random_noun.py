from api.models import GrammarQueryStub, Noun
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Gets a stream of random nouns'

    def handle(self, *args, **options):
        user = User.objects.get(pk=1)
        query_stub = GrammarQueryStub(mode='random', user=user)

        for i in range(0, 100):
            print(Noun.random(query_stub))