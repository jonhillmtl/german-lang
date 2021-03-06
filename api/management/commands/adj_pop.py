from . import DocStringCommand
from api.models import Adjective, Translation
from typing import List, Dict


class Command(DocStringCommand):
    """ Populates nouns. """

    def handle(self, *args: List, **options: Dict) -> None:
        """ The handler for this script. """

        with open("./data/de_DE/words.csv", "r") as f:
            for line in f.readlines()[1:]:
                values = line.split(';')

                if values[5] != 'adjective':
                    continue

                text = values[0]

                adj = Adjective.objects.filter(adjective=values[0]).first()
                if adj is None:
                    print("adding {}".format(text))
                    adj = Adjective()
                else:
                    print("updating {}: {}".format(adj.id, adj.adjective))

                adj.adjective = text
                adj.language_code = 'de_DE'
                adj.level = values[2]
                adj.chapter = values[3]

                adj.save()

                for nt in adj.translation_set.all():
                    nt.delete()

                if values[1] != '':
                    nt = Translation(
                        adjective=adj,
                        translation=values[1],
                        language_code='en_US')
                    nt.save()

                adj.save()
