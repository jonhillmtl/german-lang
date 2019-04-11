from api.models import Adjective, Noun
from . import DocStringCommand
from typing import List, Dict

import pprint


class Command(DocStringCommand):
    """ Declinates adjectives. """

    def handle(self, *args: List, **options: Dict) -> None:
        """ The handler for this script. """

        for adjective in Adjective.objects.all():
            noun, choice_mode = Noun.random()

            print(adjective.adjective, noun.singular_form)
            pprint.pprint(adjective.declinate(noun))
