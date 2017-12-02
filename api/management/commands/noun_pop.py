from django.core.management.base import BaseCommand, CommandError
from api.models import Noun, Translation

class Command(BaseCommand):
    help = 'Populates the nouns'

    def handle(self, *args, **options):
        with open("./data/nouns.csv", "r") as f:
            for line in f.readlines()[1:]:
                values = line.split(';')

                # TODO JHILL: add translations

                singular_form = values[0]
                singular_form = singular_form.strip()

                noun = Noun.objects.filter(singular_form=singular_form).first()
                if noun is None:
                    print("adding {}".format(singular_form))
                    noun = Noun()
                else:
                    print("updating {}: {}".format(noun.id, noun.singular_form))
                
                gender = values[2].strip().lower()
                if gender == 'das':
                    gender = 'n'
                elif gender == 'die':
                    gender = 'f'
                elif gender == 'der':
                    gender = 'm'
                elif gender not in ['n', 'f', 'm']:
                    assert False, "gender {} not recognized".format(gender)

                noun.singular_form = singular_form
                noun.plural_form = values[1]
                noun.gender = gender
                noun.language_code = 'de_DE'
                noun.level = values[5]
                noun.chapter = values[6]

                tags = [v.strip().lower() for v in values[7].split(",")]
                if tags != ['']:
                    noun.tags = tags
                else:
                    noun.tags = []

                print(tags)

                noun.save()

                for nt in noun.translation_set.all():
                    nt.delete()

                if values[3] != '':
                    nt = Translation(
                        noun=noun,
                        translation=values[3],
                        form='s',
                        language_code='en_US')
                    nt.save()

                if values[4] != '':
                    nt = Translation(
                        noun=noun,
                        translation=values[4],
                        form='p',
                        language_code='en_US')
                    nt.save()
                noun.save()