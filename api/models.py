from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Count,  Case, When, Sum, F, Value, FloatField, CharField
from django.db.models.functions import Cast

from itertools import chain
from text_header import text_header
from enum import Enum, unique

import datetime
import random

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
    ('c1', 'c1')
)

@unique
class Mode(Enum):
    NOUN_GENDER = 'noun_gender'
    NOUN_PLURALIZATION = 'noun_pluralization'
    NOUN_TRANSLATION = 'noun_translation'
    NOUN_TRANSLATION_MULTI = 'noun_translation_multi'

    VERB_PP_MULTI = 'verb_pp_multi'
    VERB_TRANSLATION_MULTI = 'verb_translation_multi'


class GrammarQueryStub(object):
    mode = None
    start_time = None
    end_time = None
    user = None
    cls = None
    count = 30

    def __init__(self, count=10, user=None, mode=None, start_time=None, end_time=None):
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

# expand to handle multiple qgm_types
class UserStats(object):
    user = None
    def __init__(self, user):
        self.user = user

    def _percentage_query(self, grammar_query_stub):
        params = grammar_query_stub.build_query_params()

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
        grammar_query_stub = GrammarQueryStub(user=self.user, mode=mode)
        return self._percentage_query(grammar_query_stub)

    def last_24h_percentage(self, mode=None):
        # TODO JHILL: fix this
        grammar_query_stub = GrammarQueryStub(user=self.user, mode=mode)
        return self._percentage_query(grammar_query_stub)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    levels = JSONField(default=list, blank=True, null=True)
    tags = JSONField(default=list, blank=True, null=True)


class GrammarQueryModel(models.Model):
    level = models.CharField(max_length=4, null=True, choices=COURSE_LEVELS, default=None)
    chapter = models.IntegerField(null=True, default=None)
    language_code = models.CharField(max_length=5)
    tags = ArrayField(base_field=CharField(max_length=32), default=list)

    # TODO JHILL: cache this!
    # there might be a prettier way to do this
    @classmethod
    def levels(cls):
        nouns = Noun.objects.values('level', 'chapter').distinct()
        verbs = Noun.objects.values('level', 'chapter').distinct()

        return nouns.union(verbs).order_by('level', 'chapter')

    # TODO JHILL: cache this!
    # there might be a prettier way to do this
    @classmethod
    def all_tags(cls):
        nouns = Noun.objects.values('tags').distinct()
        verbs = Noun.objects.values('tags').distinct()

        all_tags = nouns.union(verbs)

        tags = []
        for all_tag in all_tags:
            for _, tag in all_tag.items():
                tags.extend(tag)
        return sorted(list(set(tags)))

    class Meta:
        abstract = True

    @classmethod
    def random(cls, grammar_query_stub):
        # TODO JHILL: move somewhere nicer
        grammar_query_stub.cls = str(cls).split('.')[-1][:-2].lower()

        funcs = [
            cls.never_done,
            cls.rarely_done,
            cls.recently_wrong,
            cls.weak
        ]

        func = random.choice(funcs)
        models = func(grammar_query_stub)
        choice_mode = str(func.__name__)

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
        ).order_by("total").values_list(grammar_query_stub.cls + '_id')
        
        id_list = [m[0] for m in query[0:grammar_query_stub.count]]
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(id_list)])
        return cls.objects.filter(id__in=query).order_by(preserved)

    @classmethod
    def never_done(cls, grammar_query_stub):
        params = grammar_query_stub.build_query_params()
        grammar_query_stub.cls = str(cls).split('.')[-1][:-2].lower()
        
        query = Answer.objects.filter(
            **params,
        ).values(grammar_query_stub.cls).values_list(grammar_query_stub.cls + '_id', flat=True)

        return cls.objects.exclude(id__in=query)

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
        ).order_by("average").values_list(grammar_query_stub.cls + '_id', flat=True)

        return cls.objects.filter(id__in=query)

    @classmethod
    def recently_wrong(cls, grammar_query_stub):
        params = grammar_query_stub.build_query_params()
        grammar_query_stub.cls = str(cls).split('.')[-1][:-2].lower()

        query = Answer.objects.filter(
            **params,
            correct=False
        ).order_by('-created_at').values(grammar_query_stub.cls).values_list(grammar_query_stub.cls + '_id', flat=True)
        id_list =list(query)[0:grammar_query_stub.count]
        
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(id_list)])
        print(preserved)
        return cls.objects.filter(id__in=query).order_by(preserved)

    # TODO JHILL: this function is a mess, clean it up
    @property
    def possible_translations(self):
        translation = self.translation_set.order_by('?').first()
        fill_count = 7

        # TODO JHILL: this could be prettier
        params = dict()
        if self.__class__ == Noun:
            params['noun__isnull'] = False
        elif self.__class__ == Verb:
            params['verb__isnull'] = False

        random_translations = random.sample(
            list(Translation.objects.filter(**params).all()),
            fill_count
        )

        random_translations.append(translation)
        translations = random.sample(random_translations, 8)

        return [dict(id=t.id, translation=t.translation) for t in  translations]

    @property
    def translations_text(self):
        translations = self.translation_set.all()
        return ", ".join([pt.translation for pt in translations])

    def check_translation_id(self, translation_id):
        """ 
        check to see if this GrammarQueryModel is translated by the translation
        represented by translation_id
        :param translation_id: the id of the translation to filter for
        :return bool: true if it was in the set, false if not
        """
        return self.translation_set.filter(id=translation_id).first() is not None


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Noun(GrammarQueryModel, TimeStampedModel):
    singular_form = models.CharField(max_length=64)
    plural_form = models.CharField(max_length=64)
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
    def gendered_nominative_singular(self):
        return "{} {}".format(
            GERMAN_GENDER_DEFINITE_ARTICLES.get(self.gender, ""),
            self.singular_form
        )

    @property
    def gendered_nominative_plural(self):
        if self.plural_form == '':
            return ''

        return "{} {}".format(
            GERMAN_GENDER_DEFINITE_ARTICLES.get("f", "f"),
            self.plural_form
        )

    def check_plural(self, plural):
        # TODO JHILL: make more lenient
        return self.gendered_nominative_plural == plural

    def check_gender_correction(self, correction):
        # TODO JHILL: make more lenient
        return self.gender_correction == correction

    def check_gender(self, gender):
        return self.gender == gender

    # TODO JHILL: move to grammar query model?
    def check_translation(self, translation):
        # TODO JHILL: make more lenient
        return self.translation_set.filter(translation=translation).first() is not None

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
    verb = models.CharField(max_length=64, default='')
    past_participle = models.CharField(max_length=64, default='')
    seperable = models.BooleanField(default=False)
    irregular = models.BooleanField(default=False)
    auxiliary = models.CharField(max_length=32, default='')
    type = models.CharField(max_length=16, default='')

    def check_past_participle(self, pp):
        # TODO JHILL: make more lenient
        return self.past_participle == pp

    @property
    def possible_past_participles(self):
        translation = self.past_participle
        fill_count = 7

        # TODO JHILL: this could be prettier
        random_verbs = random.sample(
            list(Verb.objects.all()),
            fill_count
        )

        random_verbs = [v.past_participle for v in random_verbs]
        random_verbs.append(translation)

        return random.sample(random_verbs, 8)

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

