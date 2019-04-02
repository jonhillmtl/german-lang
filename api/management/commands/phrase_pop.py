from django.core.management.base import BaseCommand
from api.models import Phrase, Translation
from typing import List, Dict


class Command(BaseCommand):
    help = 'Populates the nouns'

    def handle(self, *args: List, **options: Dict) -> None:
        with open("./data/de_DE/phrases.csv", "r") as f:
            for line in f.readlines()[1:]:
                values = line.split(';')

                text = values[0]

                phrase = Phrase.objects.filter(phrase=values[0]).first()
                if phrase is None:
                    print("adding {}".format(text))
                    phrase = Phrase()
                else:
                    print("updating {}: {}".format(phrase.id, phrase.phrase))
                
                phrase.phrase = text
                phrase.language_code = 'de_DE'
                phrase.level = 'a1.1'
                phrase.chapter = 1

                phrase.save()

                for nt in phrase.translation_set.all():
                    nt.delete()

                if values[1] != '':
                    nt = Translation(
                        phrase=phrase,
                        translation=values[1],
                        language_code='en_US')
                    nt.save()

                phrase.save()