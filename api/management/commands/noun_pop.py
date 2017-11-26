from django.core.management.base import BaseCommand, CommandError
from api.models import Noun, NounTranslation

class Command(BaseCommand):
    help = 'Populates the nouns'

    def handle(self, *args, **options):
        with open("./data/nouns.csv", "r") as f:
            for line in f.readlines()[1:]:
                values = line.split(',')

                # TODO JHILL: add translations

                singular_form = values[0]
                singular_form = singular_form.strip()

                noun = Noun.objects.filter(singular_form=singular_form).first()
                if noun is None:
                    print("adding {}".format(singular_form))
                    noun = Noun()
                else:
                    print("updating {}: {}".format(noun.id, noun.singular_form))

                noun.singular_form = singular_form
                noun.plural_form = values[1]
                noun.gender = values[2]
                noun.language_code = 'de_DE'
                noun.level = values[5]
                noun.chapter = values[6]

                for nt in noun.nountranslation_set.all():
                    nt.delete()

                if values[3] != '':
                    nt = NounTranslation(
                        noun=noun,
                        answer=values[3],
                        form='s',
                        language_code='en_US')
                    nt.save()

                if values[4] != '':
                    nt = NounTranslation(
                        noun=noun,
                        answer=values[4],
                        form='p',
                        language_code='en_US')
                    nt.save()
                noun.save()