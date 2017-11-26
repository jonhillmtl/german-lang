from datetime import datetime

from django.db import connection

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer    

from rest_framework.views import APIView

from .serializers import NounSerializer
from .models import Noun, Answer, UserStats

import json
import random

def _rarely_done(us, mode):
    noun = None
    rarely_done = us.rarely_done_nouns(mode)[0:10]
    if len(rarely_done) > 0:
        noun = Noun.objects.get(pk=random.choice(rarely_done)['noun'])
    return noun, "rarely_done"
    
def _recently_wrong(us, mode):
    noun = None
    recently_wrong_nouns = us.recently_wrong_nouns(mode)[0:10]
    if len(recently_wrong_nouns) > 0:
        noun = random.choice(recently_wrong_nouns)
    return noun, "recently_wrong"
    
def _weak_noun(us, mode):
    noun = None
    weak_nouns = us.weak_nouns(mode)[0:10]
    if len(weak_nouns) > 0:
        noun = Noun.objects.get(pk=random.choice(weak_nouns)['noun'])
    return noun, "weak"
    
def _never_done_noun(us, mode):
    noun = None
    never_done_nouns = us.never_done_nouns(mode)
    if len(never_done_nouns) > 0:
        noun = random.choice(never_done_nouns)
    return noun, "never_done"

@api_view(['GET'])
def random_noun(request):
    # TODO JHILL: need to specify language code, or provide a default
    # need to specify a mode for this
    mode = 'noun_gender'

    us = UserStats(request.user)
    funcs = [_rarely_done, _recently_wrong, _weak_noun, _never_done_noun]
    noun, choice_mode = random.choice(funcs)(us, mode)

    if noun is None:
        noun = Noun.random()
        choice_mode = "random_recovery_" + choice_mode

    data = dict(
        noun=NounSerializer(noun).data,
        success=True,
        choice_mode=choice_mode
    )

    # if 'get_translations' in json_data and json_data['get_translations'] is True
    if True:
        data['translations'] = noun.possible_translations

    return JsonResponse(data, safe=False)


@api_view(['GET'])
def noun_view(request, pk):
    # TODO JHILL: handle 404 gracefuly
    noun = Noun.objects.get(pk=pk)

    return JsonResponse(dict(
        noun=NounSerializer(noun).data,
        success=True
    ), safe=False)


@api_view(['POST'])
def noun_answer_gender_check(request):
    json_data = json.loads(request.body)
    noun = Noun.objects.get(pk=json_data['noun_id'])

    try:
        results, singular_answers, plural_answers = noun.check_answers(json_data)

        return JsonResponse(dict(
            results=results,
            singular_answers=singular_answers,
            plural_answers=plural_answers,
            noun=NounSerializer(noun).data,
            success=True
        ), safe=False)
    except AssertionError as e:
        return JsonResponse(dict(
            success=False,
            error=str(e)
        ))
