from django.db import models
from django.contrib.auth.models import User
import datetime
from django.db.models import Count,  Case, When, Sum, F, Value, FloatField, CharField
from django.db.models.functions import Cast
import random

from django.contrib.postgres.fields import JSONField
from itertools import chain

from text_header import text_header

def normalize_answer(answer):
    if answer is None:
        return None

    return answer.lower().rstrip().lstrip()

# TODO JHILL: clean up
GERMAN_GENDER_DEFINITE_ARTICLES = {
    'n': 'das',
    'f': 'die',
    'm': 'der'
}

# TODO JHILL: clean up
GERMAN_GENDER_INDEFINITE_ARTICLES = {
    'n': 'ein',
    'f': 'eine',
    'm': 'ein'
}

GENDERS = (
    ('m', 'masculine'),
    ('f', 'feminine'),
    ('n', 'neuter'),
)

NOUN_FORMS = (
    ('s', 'singular'),
    ('p', 'plural'),
)

PERSON = (
    ('1', 'first'),
    ('2', 'second'),
    ('3', 'third')
)

COURSE_LEVELS = (
    ('a1.1', 'a1.1'),
    ('a1.2', 'a1.2'),
    ('a2.1', 'a2.1'),
    ('a2.2', 'a2.2'),
    ('b1.1', 'b1.2'),
    ('b2.1', 'b2.2'),
    ('c1')
)

class GrammarQueryStub(object):
    mode = None
    start_time = None
    end_time = None
    user = None
    cls = None
    count = 30

    def __init__(self, count=10, cls=None, user=None, mode=None, start_time=None, end_time=None):
        self.user = user
        self.mode = mode
        self.start_time = start_time
        self.end_time = end_time
        self.count = count

    def build_query_params(self):
        params = dict(
            user=self.user,
        )

        if self.mode is not None:
            params['mode'] = self.mode

        if self.start_time is not None:
            params['created_at__gt'] = self.start_time

        if self.end_time is not None:
            params['created_at__lt'] = self.end_time

        return params


class UserStats(object):
    user = None
    def __init__(self, user):
        self.user = user

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

class GrammarQueryModel(models.Model):
    level = models.CharField(max_length=4, null=True, choices=GENDERS, default=None)
    chapter = models.IntegerField(null=True, default=None)
    language_code = models.CharField(max_length=5)

    class Meta:
        abstract = True

    @classmethod
    def random(cls, grammar_query_stub):
        # TODO JHILL: move somewhere nicer
        grammar_query_stub.cls = str(cls).split('.')[-1][:-2].lower()

        funcs = [
            cls.never_done,
            cls.never_done,
            cls.never_done,
            cls.rarely_done,
            cls.recently_wrong,
            cls.weak
        ]

        models, choice_mode = random.choice(funcs)(grammar_query_stub)

        if models.count() == 0:
            models, choice_mode = cls.rarely_done
        
        if models.count() == 0:
            models, choice_mode = cls.objects.order_by('?'), "random"

        model = random.choice(models[0:grammar_query_stub.count])
        return model, choice_mode

    @classmethod
    def rarely_done(cls, grammar_query_stub):
        params = grammar_query_stub.build_query_params()
        grammar_query_stub.cls = str(cls).split('.')[-1][:-2].lower()

        query = Answer.objects.filter(
            **params,
        ).values(grammar_query_stub.cls).annotate(
            correct_count=Cast(Count(Case(When(correct=True, then=True))), FloatField())
        ).annotate(
            incorrect_count=Cast(Count(Case(When(correct=False, then=False))), FloatField())
        ).annotate(
            total=(F('correct_count') + F('incorrect_count'))
        ).order_by("total").values_list('noun_id', flat=True)

        return cls.objects.filter(id__in=query), "rarely_done"

    @classmethod
    def never_done(cls, grammar_query_stub):
        params = grammar_query_stub.build_query_params()
        grammar_query_stub.cls = str(cls).split('.')[-1][:-2].lower()
        
        query = Answer.objects.filter(
            **params,
        ).values(grammar_query_stub.cls).values_list('noun_id', flat=True)

        return cls.objects.exclude(id__in=query), "never_done"

    @classmethod
    def weak(cls, grammar_query_stub):
        params = grammar_query_stub.build_query_params()
        grammar_query_stub.cls = str(cls).split('.')[-1][:-2].lower()

        query = Answer.objects.filter(
            **params,
        ).values(grammar_query_stub.cls).annotate(
            correct_count=Cast(Count(Case(When(correct=True, then=True))), FloatField())
        ).annotate(
            incorrect_count=Cast(Count(Case(When(correct=False, then=False))), FloatField())
        ).annotate(
            total=(F('correct_count') + F('incorrect_count'))
        ).filter(
            total__gt=0
        ).annotate(
            average=(F('correct_count') / F('total') * 100)
        ).order_by("average").values_list('noun_id', flat=True)

        return cls.objects.filter(pk__in=query), "weak"

    @classmethod
    def recently_wrong(cls, grammar_query_stub):
        params = grammar_query_stub.build_query_params()
        grammar_query_stub.cls = str(cls).split('.')[-1][:-2].lower()

        query = Answer.objects.filter(
            **params,
            correct=False
        ).values('noun_id').values_list('noun_id', flat=True)

        return cls.objects.filter(pk__in=query), "recently_wrong"

    @property
    def possible_translations(self):
        translations = self.translation_set.filter(form='s')
        fill_count = 8 - len(translations)

        random_translations = random.sample(list(Translation.objects.filter(form='s').all()), fill_count)
        translations = list(chain(translations, random_translations))

        return [dict(id=t.id, translation=t.translation) for t in random.sample(translations, 8)]
        
    @property
    def translations_text(self):
        translations = self.translation_set.all()
        return ", ".join([pt.translation for pt in translations])

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Noun(GrammarQueryModel, TimeStampedModel):
    singular_form = models.CharField(max_length=128)
    plural_form = models.CharField(max_length=128)
    gender = models.CharField(max_length=1, choices=GENDERS)

    def answers(self, form, target_language_code):
        assert form in [f[0] for f in NOUN_FORMS], "{} not in NOUN_FORMS".format(form)
        return [normalize_answer(na.translation) for na in Translation.objects.filter(
            noun=self,
            form=form,
            language_code=target_language_code
        ).all()]

    @property
    def gender_correction(self):
        # TODO JHILL: definitely want to have some sort of language_code switcher here
        return "{} {}".format(
            GERMAN_GENDER_DEFINITE_ARTICLES.get(self.gender, ""),
            self.singular_form
        )

    @property
    def gendered_singular(self):
        return "{} {}".format(
            GERMAN_GENDER_DEFINITE_ARTICLES.get(self.gender, ""),
            self.singular_form
        )

    @property
    def gendered_plural(self):
        if self.plural_form == '':
            return ''

        return "{} {}".format(
            GERMAN_GENDER_DEFINITE_ARTICLES.get("f", "f"),
            self.plural_form
        )

    def check_plural(self, plural):
        # TODO JHILL: make more lenient
        return self.gendered_plural == plural

    def check_gender_correction(self, correction):
        # TODO JHILL: make more lenient
        return self.gender_correction == correction

    def check_gender(self, gender):
        return self.gender == gender

    # TODO JHILL: move to grammar query model?
    def check_translation(self, translation_id):
        return self.translation_set.filter(id=translation_id).first() is not None

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


class Verb(GrammarQueryModel, TimeStampedModel):
    pass

class Preposition(GrammarQueryModel, TimeStampedModel):
    pass

class Pronoun(GrammarQueryModel, TimeStampedModel):
    pass

class Adjective(GrammarQueryModel, TimeStampedModel):
    pass

class Adverb(GrammarQueryModel, TimeStampedModel):
    pass

class Phrase(GrammarQueryModel, TimeStampedModel):
    pass
    

class Translation(TimeStampedModel):
    noun = models.ForeignKey(Noun, null=True)
    verb = models.ForeignKey(Verb, null=True)

    translation = models.CharField(max_length=512)
    form = models.CharField(max_length=1, choices=NOUN_FORMS)
    language_code = models.CharField(max_length=5, default='en_US')

    def __str__(self):
        return "{}: {} ({}) ({})".format(
            self.noun,
            self.translation,
            self.form,
            self.language_code)


class Answer(TimeStampedModel):
    noun = models.ForeignKey(Noun, null=True)
    verb = models.ForeignKey(Verb, null=True)

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
            

