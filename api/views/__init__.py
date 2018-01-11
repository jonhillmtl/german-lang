from datetime import datetime

from django.db import connection

from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer    

from rest_framework.views import APIView

from ..serializers import NounSerializer, VerbSerializer, NounFlashSerializer, AdjectiveSerializer, PhraseSerializer
from ..models import Noun, Answer, UserStats, GrammarQueryStub, Verb, Adjective, Phrase

import json
import random
from text_header import text_header

@api_view(['GET'])
def nouns(request):
    return JsonResponse(data=dict(
        nouns=NounFlashSerializer(Noun.objects.all(), many=True).data
    ))

@api_view(['GET'])
def noun_random(request):
    # TODO JHILL: need to specify language code, or provide a default
    # need to specify a mode for this
    # TODO JHILL: make into a general purpose view for all GrammarQueryModels
    # very important here!
    assert request.method == 'GET'

    mode = request.GET.get('mode', None)

    query_stub = GrammarQueryStub(mode=mode, user=request.user)

    if mode == 'noun_plurazation':    
        while True:
            noun, choice_mode = Noun.random(grammar_query_stub=query_stub)
            if noun.plural_form != '':
                break
    else:
        noun, choice_mode = Noun.random(grammar_query_stub=query_stub)

    data = dict(
        noun=NounSerializer(noun).data,
        success=True,
        choice_mode=choice_mode,
        mode=mode
    )

    return JsonResponse(data, safe=False)

@api_view(['GET'])
def verb_random(request):
    # TODO JHILL: need to specify language code, or provide a default
    # need to specify a mode for this
    # TODO JHILL: make into a general purpose view for all GrammarQueryModels
    # very important here!
    assert request.method == 'GET'

    mode = request.GET.get('mode', None)

    query_stub = GrammarQueryStub(mode=mode, user=request.user)
    verb, choice_mode = Verb.random(grammar_query_stub=query_stub)

    data = dict(
        verb=VerbSerializer(verb).data,
        success=True,
        choice_mode=choice_mode,
        mode=mode
    )

    return JsonResponse(data, safe=False)
    
@api_view(['GET'])
def adjective_random(request):
    # TODO JHILL: need to specify language code, or provide a default
    # need to specify a mode for this
    # TODO JHILL: make into a general purpose view for all GrammarQueryModels
    # very important here!
    assert request.method == 'GET'

    mode = request.GET.get('mode', None)

    query_stub = GrammarQueryStub(mode=mode, user=request.user)
    adjective, choice_mode = Adjective.random(grammar_query_stub=query_stub)

    data = dict(
        adjective=AdjectiveSerializer(adjective).data,
        success=True,
        choice_mode=choice_mode,
        mode=mode
    )

    return JsonResponse(data, safe=False)
    
@api_view(['GET'])
def phrase_random(request):
    # TODO JHILL: need to specify language code, or provide a default
    # need to specify a mode for this
    # TODO JHILL: make into a general purpose view for all GrammarQueryModels
    # very important here!
    assert request.method == 'GET'

    mode = request.GET.get('mode', None)

    query_stub = GrammarQueryStub(mode=mode, user=request.user)
    phrase, choice_mode = Phrase.random(grammar_query_stub=query_stub)

    data = dict(
        phrase=PhraseSerializer(phrase).data,
        success=True,
        choice_mode=choice_mode,
        mode=mode
    )

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

@api_view(['GET'])
def stats(request):
    # TODO JHILL: Move this onto the user object, make it queryable like crazy
    us = UserStats(request.user)
    mode = request.GET.get('mode', None)
    gqm_type = request.GET.get('gqm_type', None)

    return JsonResponse(dict(
        mode_percentage=us.all_time_percentage(mode),
        all_time_percentage=us.all_time_percentage(),
        succces=True
    ))
