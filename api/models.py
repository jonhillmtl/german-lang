from django.db import models
from utils import GENDERS, NOUN_FORMS, COURSE_LEVELS, PERSON
from django.contrib.auth.models import User
import datetime
from django.db.models import Count,  Case, When, Sum, F, Value, FloatField, CharField
from django.db.models.functions import Cast
import random

from django.contrib.postgres.fields import JSONField
from itertools import chain

def normalize_answer(answer):
    if answer is None:
        return None

    return answer.lower().rstrip().lstrip()

GERMAN_GENDER_DEFINITE_ARTICLES = {
    'n': 'das',
    'f': 'die',
    'm': 'der'
}

GERMAN_GENDER_INDEFINITE_ARTICLES = {
    'n': 'ein',
    'f': 'eine',
    'm': 'ein'
}

class UserStats(object):
    user = None
    def __init__(self, user):
        self.user = user

    def _build_query_params(self, mode=None, start_time=None, end_time=None):
        params = dict(
            user=self.user,
        )

        if mode is not None:
            params['mode']   = mode

        if start_time is not None:
            params['created_at__gt'] = start_time

        if end_time is not None:
            params['created_at__lt'] = end_time

        return params

    def _percentage_query(self, mode=None, start_time=None, end_time=None):
        params = self._build_query_params(mode, start_time, end_time)

        correct = Answer.objects.filter(
            **params,
            correct=True
        ).count()

        incorrect = Answer.objects.filter(
            **params,
            correct=False
        ).count()

        total = correct + incorrect
        if total is 0:
            return None

        return correct / total * 100.0

    def all_time_percentage(self, mode=None):
        return self._percentage_query(mode=mode)

    def last_24h_percentage(self, mode=None):
        return self._percentage_query(
            mode=mode,
            start_time=datetime.datetime.now() - datetime.timedelta(days=1))

    # TODO JHILL: collapse this and check the results, it seems fishy
    def rarely_done_nouns(self, mode=None, start_time=None, end_time=None):
        params = self._build_query_params(mode, start_time, end_time)

        return Answer.objects.filter(
            **params,
        ).values('noun').annotate(
            correct_count=Cast(Count(Case(When(correct=True, then=True))), FloatField())
        ).annotate(
            incorrect_count=Cast(Count(Case(When(correct=False, then=False))), FloatField())
        ).annotate(
            total=(F('correct_count') + F('incorrect_count'))
        ).order_by("total")
        
    # TODO JHILL: collapse this and check the results, it seems fishy
    def recently_wrong_nouns(self, mode=None, start_time=None, end_time=None):
        params = self._build_query_params(mode, start_time, end_time)
        recently_wrong_nouns = Answer.objects.filter(
            **params,
            correct=False
        ).values('noun')
        
        return Noun.objects.filter(id__in=[dn['noun'] for dn in recently_wrong_nouns])

    # TODO JHILL: collapse this and check the results, it seems fishy
    def never_done_nouns(self, mode=None, start_time=None, end_time=None):
        params = self._build_query_params(mode, start_time, end_time)
        done_nouns = Answer.objects.filter(
            **params,
        ).values('noun')

        return Noun.objects.exclude(id__in=[dn['noun'] for dn in done_nouns])

    # TODO JHILL: collapse this and check the results, it seems fishy
    def weak_nouns(self, mode=None, start_time=None, end_time=None):
        params = self._build_query_params(mode, start_time, end_time)

        return Answer.objects.filter(
            **params,
        ).values('noun').annotate(
            correct_count=Cast(Count(Case(When(correct=True, then=True))), FloatField())
        ).annotate(
            incorrect_count=Cast(Count(Case(When(correct=False, then=False))), FloatField())
        ).annotate(
            total=(F('correct_count') + F('incorrect_count'))
        ).filter(
            total__gt=0
        ).annotate(
            average=(F('correct_count') / F('total') * 100)
        ).order_by("average")


class GrammarQueryModel(models.Model):
    level = models.CharField(max_length=4, null=True, choices=GENDERS, default=None)
    chapter = models.IntegerField(null=True, default=None)
    language_code = models.CharField(max_length=5)

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
    gender = models.CharField(max_length=1, choices=GENDERS)

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
        return "{} {}".format(
            GERMAN_GENDER_DEFINITE_ARTICLES.get(self.gender, ""),
            self.singular_form
        )

    def check_gender_correction(self, correction):
        # TODO JHILL: make more lenient
        return self.gender_correction == correction

    def check_gender(self, gender):
        return self.gender == gender
        
    def check_translation(self, translation_id):
        return self.nountranslation_set.filter(id=translation_id).first() is not None
    
    @property
    def possible_translations(self):
        # TODO JHILL: this is probably crazy slow
        correct_translations = self.nountranslation_set.filter(noun=self, form='s').all()
        fill_count = 8 - len(correct_translations)
        
        random_translations = random.sample(list(NounTranslation.objects.filter(form='s').all()), fill_count)
        translations = list(chain(random_translations, correct_translations))

        return random.sample([dict(id=nt.id, answer=nt.answer) for nt in translations], 8)

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
    mode = models.CharField(max_length=32, default='')

    answer = JSONField(default='{}')
    correction = models.BooleanField(default=False)
    correct_answer = models.CharField(max_length=512, default='')

    def __str__(self):
        return "({}) ({})".format(
            self.correct,
            self.correction)
            

