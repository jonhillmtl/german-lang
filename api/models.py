from django.db import models
from utils import GENDERS, NOUN_FORMS, COURSE_LEVELS, PERSON
from django.contrib.auth.models import User

from django.contrib.postgres.fields import JSONField

def normalize_answer(answer):
    if answer is None:
        return None

    return answer.lower().rstrip().lstrip()

GERMAN_GENDER_DEFINITE_ARTICLES = {
    'n': 'das',
    'f': 'die',
    'm': 'der'
}

class GrammarQueryModel(models.Model):
    level = models.CharField(max_length=2, null=True, choices=GENDERS, default=None)
    chapter = models.IntegerField(null=True, default=None)

    class Meta:
        abstract = True

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Noun(GrammarQueryModel, TimeStampedModel):
    singular_form = models.CharField(max_length=128)
    plural_form = models.CharField(max_length=128)
    language_code = models.CharField(max_length=5)
    gender = models.CharField(max_length=1, choices=GENDERS)

    notes = models.TextField(null=True, blank=True)

    @staticmethod
    def random():
        # TODO JHILL: need to specify language code or have a default
        # TODO JHILL: this is slow, find a better way
        return Noun.objects.order_by('?').first()

    def answers(self, form, target_language_code):
        assert form in [f[0] for f in NOUN_FORMS], "{} not in NOUN_FORMS".format(form)
        return [normalize_answer(na.answer) for na in NounTranslation.objects.filter(
            noun=self,
            form=form,
            language_code=target_language_code
        ).all()]

    @property
    def gender_correction(self):
        print(self)
        correction = "{} {}".format(
            GERMAN_GENDER_DEFINITE_ARTICLES.get(self.gender, ""),
            self.singular_form
        )
        return correction

    def check_gender_correction(self, correction):
        # TODO JHILL: make more lenient
        print(correction, self.gender_correction)
        return correction == self.gender_correction

    def check_gender(self, gender):
        return self.gender == gender, self.gender_correction

    def check_answers(self, data):
        target_language_code = data.get('target_language_code', None)
        gender = data.get('gender', None)
        singular_form = normalize_answer(data.get('singular_form', None))
        plural_form = normalize_answer(data.get('plural_form', None))
        
        assert plural_form is not None, 'Must provide plural_form'
        assert singular_form is not None, 'Must provide singular_form'
        assert gender is not None, 'Must provide gender'
        assert target_language_code is not None, 'Must provide target_language_code'

        singular_answers = self.answers('s', target_language_code)
        plural_answers = self.answers('p', target_language_code)

        assert len(singular_answers) > 0, "Noun {}: {}  misconfigured, no singular_answers for {}".format(
            self.id,
            self,
            target_language_code)
        assert len(plural_answers) > 0, "Nound {}: {} misconfigured, no plural_answers for {}".format(
            self.id,
            self,
            target_language_code)

        singular_correct = (singular_form in singular_answers)
        plural_correct = (plural_form in plural_answers)
        gender_correct = (self.gender == gender)
        correct = singular_correct and plural_correct and gender_correct

        return dict(
            correct=correct,
            singular_correct=singular_correct,
            plural_correct=plural_correct,
            gender_correct=gender_correct
        ), singular_answers, plural_answers

    def __str__(self):
        return "{}/{} ({}) ({})".format(
            self.singular_form,
            self.plural_form,
            self.gender,
            self.language_code)


class NounTranslation(TimeStampedModel):
    noun = models.ForeignKey(Noun)
    answer = models.CharField(max_length=128)
    form = models.CharField(max_length=1, choices=NOUN_FORMS)
    notes = models.TextField(null=True, blank=True)
    language_code = models.CharField(max_length=5, default='en_US')

    def __str__(self):
        return "{}: {} ({}) ({})".format(
            self.noun,
            self.answer,
            self.form,
            self.language_code)


class Answer(TimeStampedModel):
    noun = models.ForeignKey(Noun, null=True)

    user = models.ForeignKey(User)
    correct = models.BooleanField(default=False)
    mode = models.CharField(max_length=16, default='')

    answer = JSONField(default='{}')
    correction = models.BooleanField(default=False)
    correct_answer = models.CharField(max_length=512, default='')

    def __str__(self):
        return "({}) ({})".format(
            self.correct,
            self.correction)
