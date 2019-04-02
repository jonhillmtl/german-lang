from django.core.management.base import BaseCommand
from api.models import Verb, Translation

class Command(BaseCommand):
    help = 'Populates the verbs'

    def handle(self, *args, **options):
        with open("./data/de_DE/verbs.csv", "r") as f:
            for line in f.readlines()[1:]:
                values = line.split(';')

                verb_text = values[0]
                if verb_text == '':
                    continue

                verb = Verb.objects.filter(verb=verb_text).first()
                if verb is None:
                    print("adding {}".format(verb_text))
                    verb = Verb()
                else:
                    print("updating {}: {}".format(verb.id, verb.verb))

                verb.verb = verb_text
                verb.language_code = 'de_DE'
                verb.past_participle = values[2]
                verb.auxiliary = values[3]
                verb.level = values[4]
                verb.chapter = values[5] if values[5] != '' else 0
                verb.save()

                for nt in verb.translation_set.all():
                    nt.delete()

                if values[1] != '':
                    nt = Translation(
                        verb=verb,
                        translation=values[1],
                        language_code='en_US')
                    nt.save()

                verb.save()