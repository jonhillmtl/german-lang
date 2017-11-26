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

@api_view(['GET'])
def random_noun(request):
    # TODO JHILL: need to specify language code, or provide a default
    noun = Noun.random()

    return JsonResponse(dict(
        noun=NounSerializer(noun).data,
        success=True
    ), safe=False)


@api_view(['GET'])
def noun_view(request, pk):
    # TODO JHILL: handle 404 gracefuly
    noun = Noun.objects.get(pk=pk)

    return JsonResponse(dict(
        noun=NounSerializer(noun).data,
        success=True
    ), safe=False)

@api_view(['POST'])
def noun_gender_check(request):
    # TODO JHILL: handle 404 gracefuly
    json_data = json.loads(request.body)
    noun = Noun.objects.get(pk=json_data['noun_id'])

    try:
        json_data = json.loads(request.body)
        correct, correction_hint = noun.check_gender(json_data['gender'])

        answer = Answer(
            noun=noun,
            correct=correct,
            user=request.user,
            mode='noun_gender',
            correct_answer=noun.gender,
            answer=json_data,
            correction=False)
        answer.save()

        return JsonResponse(dict(
            results=correct,
            correct_answer=noun.gender,
            correction_hint=correction_hint,
            noun=NounSerializer(noun).data,
            success=True
        ), safe=False)
    except AssertionError as e:
        return JsonResponse(dict(
            success=False,
            error=str(e)
        ))

@api_view(['POST'])
def noun_gender_check_correction(request):
    json_data = json.loads(request.body)
    noun = Noun.objects.get(pk=json_data['noun_id'])

    try:
        json_data = json.loads(request.body)
        correct = noun.check_gender_correction(json_data['correction'])

        answer = Answer(
            noun=noun,            
            correct=correct,
            user=request.user,
            mode='noun_gender',
            correct_answer=noun.gender_correction,
            answer=json_data,
            correction=True)
        answer.save()

        return JsonResponse(dict(
            success=correct,
            correct_answer=noun.gender,
            answer=json_data
        ), safe=False)
    except AssertionError as e:
        return JsonResponse(dict(
            success=False,
            error=str(e)
        ))

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


def noun_gender_stats(request):
    # TODO JHILL: Move this onto the user object, make it queryable like crazy
    us = UserStats(request.user)

    return JsonResponse(dict(
        mode_percentage=us.all_time_percentage('noun_gender'),
        all_time_percentage=us.all_time_percentage(),

        mode_last_24h_percentage=us.last_24h_percentage('noun_gender'),
        last_24h_percentage=us.last_24h_percentage(),
        
        succces=True
    ))