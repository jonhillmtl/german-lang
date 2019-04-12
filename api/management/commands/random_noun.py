from api.models import GrammarQueryStub, Noun
from django.contrib.auth.models import User
from . import DocStringCommand
from typing import List, Dict


class Command(DocStringCommand):
    help = 'Gets a stream of random nouns'

    def handle(self, *args: List, **options: Dict) -> None:
        """ The handler for this script. """

        user = User.objects.get(pk=1)
        query_stub = GrammarQueryStub(mode='random', user=user)

        for i in range(0, 100):
            print(Noun.random(query_stub))
