from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Count, When, F, FloatField, CharField
from django.db.models import Case as FilterCase
from django.db.models.functions import Cast

from typing import List, Tuple, Dict, Optional, Any
from enum import Enum, unique
from difflib import SequenceMatcher

import json
import random
import datetime


def normalize_answer(answer: str) -> str:
    if answer is None:
        return None

    return answer.lower().rstrip().lstrip()


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
class Article(Enum):
    DEFINITE = 'definite'
    INDEFINITE = 'indefinite'


@unique
class Case(Enum):
    NOMINATIVE = 'nominative'
    ACCUSATIVE = 'accusative'
    DATIVE = 'dative'
    GENITIVE = 'genitive'


@unique
class Mode(Enum):
    NOUN_GENDER = 'noun_gender'
    NOUN_PLURALIZATION = 'noun_pluralization'
    NOUN_TRANSLATION = 'noun_translation'
    NOUN_TRANSLATION_MULTI = 'noun_translation_multi'

    VERB_PP_MULTI = 'verb_pp_multi'
    VERB_TRANSLATION_MULTI = 'verb_translation_multi'


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class GrammarQueryStub(object):
    mode = None
    start_time = None
    end_time = None
    user = None
    cls = None
    count = 30

    def __init__(
        self,
        count: Optional[int] = 10,
        user: Optional[User] = None,
        mode: Optional[str] = None,
        start_time: Optional[datetime.datetime] = None,
        end_time: Optional[datetime.datetime] = None
    ):
        self.user = user
        self.mode = mode
        self.start_time = start_time
        self.end_time = end_time
        self.count = count

    def build_query_params(self) -> Dict:
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

    def __init__(self, user: User):
        self.user = user

    def _percentage_query(
        self,
        grammar_query_stub: GrammarQueryStub
    ) -> Optional[float]:
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
        if total == 0:
            return None

        return correct / total * 100.0

    def all_time_percentage(self, mode: str = None) -> float:
        grammar_query_stub = GrammarQueryStub(user=self.user, mode=mode)
        return self._percentage_query(grammar_query_stub)

    def last_24h_percentage(self, mode: str = None) -> float:
        # TODO JHILL: fix this
        grammar_query_stub = GrammarQueryStub(user=self.user, mode=mode)
        return self._percentage_query(grammar_query_stub)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    levels = JSONField(default=list, blank=True, null=True)
    tags = JSONField(default=list, blank=True, null=True)


def level_chapter_valid(
    model: Any,
    level_chapters: Dict
) -> bool:
    return {'level': model.level, 'chapter': model.chapter} in level_chapters


def filter_level_chapter(
    grammar_query_stub: GrammarQueryStub,
    models: List
) -> List:
    level_chapters = grammar_query_stub.user.profile.levels
    models = models.all()
    models = [m for m in models if level_chapter_valid(m, level_chapters)]
    return models


class GrammarQueryModel(TimeStampedModel):
    level = models.CharField(max_length=4, null=True, choices=COURSE_LEVELS, default=None)
    chapter = models.IntegerField(null=True, default=None)
    language_code = models.CharField(max_length=5)
    tags = ArrayField(base_field=CharField(max_length=32), default=list)

    # TODO JHILL: cache this!
    @classmethod
    def levels(cls) -> List:
        nouns = Noun.objects.values('level', 'chapter').distinct()
        verbs = Noun.objects.values('level', 'chapter').distinct()

        return nouns.union(verbs).order_by('level', 'chapter')

    # TODO JHILL: cache this!
    @classmethod
    def all_tags(cls) -> List:
        nouns = Noun.objects.values('tags').distinct()
        verbs = Noun.objects.values('tags').distinct()

        all_tags = nouns.union(verbs)

        tags = []  # type: List
        for all_tag in all_tags:
            for _, tag in all_tag.items():
                tags.extend(tag)
        return sorted(list(set(tags)))

    class Meta:
        abstract = True

    @classmethod
    def random(cls, grammar_query_stub: Any = None) -> Tuple[Any, str]:
        if grammar_query_stub is None:
            return random.choice(cls.objects.all()), "random"

        # TODO JHILL: move somewhere nicer
        grammar_query_stub.cls = str(cls).split('.')[-1][:-2].lower()

        """
        funcs = [
            # cls.never_done,
            # cls.rarely_done,
            # cls.recently_wrong,
            cls.weak
        ]

        func = random.choice(funcs)
        models = func(grammar_query_stub)
        choice_mode = str(func.__name__)
        """

        models = cls.objects
        models = filter_level_chapter(grammar_query_stub, models)
        choice_mode = 'filtered'

        model = random.choice(models)
        return model, choice_mode

    @classmethod
    def rarely_done(cls, grammar_query_stub: GrammarQueryStub) -> List:
        params = grammar_query_stub.build_query_params()

        query = Answer.objects.filter(
            **params,
        ).values(grammar_query_stub.cls).annotate(
            correct_count=Cast(Count(FilterCase(When(correct=True, then=True))), FloatField())
        ).annotate(
            incorrect_count=Cast(Count(FilterCase(When(correct=False, then=False))), FloatField())
        ).annotate(
            total=(F('correct_count') + F('incorrect_count'))
        ).order_by("total").values_list(grammar_query_stub.cls + '_id')

        # TODO JHILL: preserved should work?
        # id_list = [m[0] for m in query[0:grammar_query_stub.count]]
        # preserved = FilterCase(*[When(pk=pk, then=pos) for pos, pk in enumerate(id_list)])
        return cls.objects.filter(id__in=query)  # .order_by(preserved)

    @classmethod
    def never_done(cls, grammar_query_stub: GrammarQueryStub) -> List:
        params = grammar_query_stub.build_query_params()

        query = Answer.objects.filter(
            **params,
        ).values(grammar_query_stub.cls).values_list(grammar_query_stub.cls + '_id', flat=True)

        return cls.objects.exclude(id__in=query)

    @classmethod
    def weak(cls, grammar_query_stub: GrammarQueryStub) -> List:
        params = grammar_query_stub.build_query_params()
        print(params)

        query = Answer.objects.filter(
            **params
        ).all()  # .values(grammar_query_stub.cls + '_id')
        print(query)

        return cls.objects.filter(id__in=query)

    @classmethod
    def recently_wrong(cls, grammar_query_stub: GrammarQueryStub) -> Any:
        params = grammar_query_stub.build_query_params()

        query = Answer.objects.filter(
            **params,
            correct=False
        ).order_by('-created_at').values(grammar_query_stub.cls).values_list(grammar_query_stub.cls + '_id', flat=True)

        id_list = list(query)[0:grammar_query_stub.count]
        preserved = FilterCase(*[When(pk=pk, then=pos) for pos, pk in enumerate(id_list)])
        return cls.objects.filter(id__in=query).order_by(preserved)

    @property
    def possible_translations(self) -> List:
        translation = self.translation_set.order_by('?').first()
        fill_count = 3

        # TODO JHILL: this could be prettier
        params = dict()
        if self.__class__ == Noun:
            params['noun__isnull'] = False

        elif self.__class__ == Verb:
            params['verb__isnull'] = False

        elif self.__class__ == Adjective:
            params['adjective__isnull'] = False

        elif self.__class__ == Phrase:
            params['phrase__isnull'] = False

        random_translations = random.sample(
            list(Translation.objects.filter(**params).all()),
            fill_count
        )

        random_translations.append(translation)
        translations = random.sample(random_translations, 4)

        return [dict(id=t.id, translation=t.translation) for t in translations]

    @property
    def translations_text(self) -> str:
        translations = self.translation_set.all()
        translations.reverse()
        return ", ".join([pt.translation for pt in translations])

    def check_translation_id(self, translation_id: int) -> bool:
        """
        check to see if this GrammarQueryModel is translated by the translation
        represented by translation_id
        :param translation_id: the id of the translation to filter for
        :return bool: true if it was in the set, false if not
        """

        return self.translation_set.filter(id=translation_id).first() is not None

    def check_translation(self, translation: str) -> bool:
        translation = translation.lower().strip()
        for trans in self.translation_set.all():
            ratio = SequenceMatcher(None, translation, trans.translation).ratio()
            if ratio >= 0.85:
                return True
        return False


# TODO JHILL: cache
def _articles(
    singular_form: Optional[str] = None,
    plural_form: Optional[str] = None,
    gender: Optional[str] = None,
    language_code: str = 'de_DE',
    append_noun: bool = False
) -> Dict:
    articles = dict()

    with open("./data/{}/articles.json".format(language_code)) as f:
        article_data = json.loads(f.read())
        for article in Article:
            for case in Case:
                for singular in [True, False]:
                    key = "{}_{}_{}".format(
                        case.value,
                        article.value,
                        'singular' if singular else 'plural'
                    )

                    if singular is False:
                        use_gender = 'p'
                    else:
                        use_gender = gender

                    if append_noun:
                        value = "{} {}".format(
                            article_data[case.value][article.value][use_gender],
                            singular_form if singular else plural_form
                        )
                    else:
                        value = "{}".format(
                            article_data[case.value][article.value][use_gender],
                        )

                    if value is not None:
                        articles[key] = value

    return articles


class Noun(GrammarQueryModel):
    singular_form = models.CharField(max_length=64)
    plural_form = models.CharField(max_length=64)
    gender = models.CharField(max_length=1, choices=GENDERS)

    def answers(
        self,
        form: str,
        target_language_code: str
    ) -> List:
        assert form in [f[0] for f in NOUN_FORMS], "{} not in NOUN_FORMS".format(form)
        return [normalize_answer(na.translation) for na in Translation.objects.filter(
            noun=self,
            form=form,
            language_code=target_language_code
        ).all()]

    @property
    def articles(self) -> Dict:
        return _articles(
            gender=self.gender
        )

    @property
    def articled(self) -> Dict:
        return _articles(
            gender=self.gender,
            plural_form=self.plural_form,
            singular_form=self.singular_form,
            language_code=self.language_code,
            append_noun=True)

    def check_plural(
        self,
        plural: str
    ) -> bool:
        # TODO JHILL: make more lenient
        # TODO JHILL: well, this depends on other things now
        return self.articled['nominative_definite_plural'] == plural

    def check_gender_correction(
        self,
        correction: str,
        article: str = 'definite',
        case: str = 'nominative'
    ) -> bool:
        key = "{}_{}_{}".format(
            case,
            article,
            'singular'
        )
        return self.articled[key] == correction

    def check_gender(self, gender: str) -> str:
        return self.gender == gender

    def check_answers(self, data: Dict) -> Tuple[Dict, List, List]:
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

    def __str__(self) -> str:
        return "{}/{} ({}) ({})".format(
            self.singular_form,
            self.plural_form,
            self.gender,
            self.language_code)


class Verb(GrammarQueryModel):
    verb = models.CharField(max_length=64, default='')
    past_participle = models.CharField(max_length=64, default='')
    seperable = models.BooleanField(default=False)
    irregular = models.BooleanField(default=False)
    auxiliary = models.CharField(max_length=32, default='')
    type = models.CharField(max_length=16, default='')

    def check_past_participle(self, pp: str) -> bool:
        # TODO JHILL: make more lenient
        return self.past_participle == pp

    @property
    def possible_past_participles(self) -> List:
        translation = self.past_participle
        fill_count = 3

        # TODO JHILL: this could be prettier
        random_verbs = random.sample(
            list(Verb.objects.all()),
            fill_count
        )

        random_verbs = [v.past_participle for v in random_verbs]
        random_verbs.append(translation)

        return random.sample(random_verbs, 4)


class Preposition(GrammarQueryModel):
    pass


class Pronoun(GrammarQueryModel):
    pass


# TODO JHILL: move somewhere nicer
# TODO JHILL: only works for German
articles = {
    'n': 'ein',
    'f': 'eine',
    'm': 'ein'
}


# TODO JHILL: move somewhere nicer
# TODO JHILL: only works for German
NOMINATIVE_DECLINATIONS = {
    'm': 'r',
    'n': 's',
    'f': 'e'
}


class Adjective(GrammarQueryModel):
    adjective = models.CharField(max_length=64, default='')

    def declinate(self, noun: Noun) -> str:
        language_code = 'de_DE'
        with open("./data/{}/articles.json".format(language_code)) as f:
            article_data = json.loads(f.read())

        with open("./data/{}/declinations.json".format(language_code)) as f:
            declination_data = json.loads(f.read())

        declinations = dict()
        for article in Article:
            for case in Case:
                key = "{}_{}".format(
                    case.value,
                    article.value
                )

                declinated = "{}{}".format(
                    self.adjective,
                    declination_data[case.value][article.value][noun.gender])

                value = "{} {} {}".format(
                    article_data[case.value][article.value][noun.gender],
                    declinated,
                    noun.singular_form
                )

                declinations[key] = value

        return declinations

    # TODO JHILL: other cases, needs to be spun out into JSON file probably
    def _declinate(self, noun: Noun) -> str:
        article = articles[noun.gender]
        declinated = ''

        if noun.gender == 'n' or noun.gender == 'm':
            format_string = ''

            if noun.singular_form[-1] == 'e':
                format_string = '{}{}'
            else:
                format_string = '{}e{}'
            declinated = format_string.format(self.adjective, NOMINATIVE_DECLINATIONS[noun.gender])

        elif noun.gender == 'f':
            format_string = ''

            if noun.singular_form[-1] == 'e':
                declinated = self.adjective
            else:
                declinated = "{}{}".format(self.adjective, NOMINATIVE_DECLINATIONS[noun.gender])

        return "{} {} {} ({})".format(article, declinated, noun.singular_form, noun.gender)

    def __str__(self) -> str:
        return "{}".format(self.adjective)


class Adverb(GrammarQueryModel):
    pass


class Phrase(GrammarQueryModel):
    phrase = models.TextField(default='')

    def __str__(self) -> str:
        return "{}".format(self.phrase)


class Translation(TimeStampedModel):
    noun = models.ForeignKey(Noun, null=True)
    verb = models.ForeignKey(Verb, null=True)
    adjective = models.ForeignKey(Adjective, null=True)
    phrase = models.ForeignKey(Phrase, null=True)

    translation = models.CharField(max_length=512)
    form = models.CharField(max_length=1, choices=NOUN_FORMS)
    language_code = models.CharField(max_length=5, default='en_US')

    # TODO JHILL: improve
    def __str__(self) -> str:
        return "{}: {} ({}) ({})".format(
            self.noun,
            self.translation,
            self.form,
            self.language_code)


class Answer(TimeStampedModel):
    noun = models.ForeignKey(Noun, null=True)
    verb = models.ForeignKey(Verb, null=True)
    adjective = models.ForeignKey(Adjective, null=True)
    phrase = models.ForeignKey(Phrase, null=True)

    user = models.ForeignKey(User)
    correct = models.BooleanField(default=False)
    mode = models.CharField(max_length=32, default='')

    answer = JSONField(default='{}')
    correction = models.BooleanField(default=False)
    correct_answer = models.CharField(max_length=512, default='')

    # TODO JHILL: improve
    def __str__(self) -> str:
        return "({}) ({})".format(
            self.correct,
            self.correction)


class AppSession(TimeStampedModel):
    finished_at = models.DateTimeField(default=None, null=True, blank=True)

    answers = models.ManyToManyField(Answer)

    user = models.ForeignKey(User)

    app_name = models.CharField(max_length=64, blank=False, null=False)

    total_count = models.IntegerField(default=0)
    correct_count = models.IntegerField(default=0)

    def update(self, answer: Answer) -> bool:
        self.answers.add(answer)

        self.total_count = self.total_count + 1

        if answer.correct:
            self.correct_count = self.correct_count + 1

        self.save()

        return True
